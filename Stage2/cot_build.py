import argparse
import copy
import asyncio
import json
import random
import re
import traceback
from call_llm import *

from datasets import load_dataset




import multiprocessing as mp
import multiprocessing
mp.set_start_method("fork")
multiprocessing.Queue(5)


from cot_prompt_en import verify_prompt, search_strategies, \
    gen_prompt_w_label, reformat_to_complex_cot_prompt, get_final_response_prompt, query_Composite_prompt_init, \
    Composite_prompt_afteragentsdoublecheck, search_strategies_subagents

from subagents import agents_initialreason, judge_if_agents_nochange_sameerror, agents_double_check, agents_communication, agents_gen_with_label
import sys




def extract_bracket_content(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else None


def parse_gpt_response(response):
    try:
        if '{' != response[0]:
            response = extract_bracket_content(response)
        da = json.loads(response.replace('\n', ''))
        assert isinstance(da["CoT"], list), "CoT should be list"
        assert da['CoT'][-3]['action'] == 'Inner Thinking', 'Inner Thinking should be the third last action'
        assert da['CoT'][-2]['action'] == 'Final Conclusion', 'Final Conclusion should be the second last action'
        assert da['CoT'][-1]['action'] == 'Verification', 'Verification should be the last action'
        return True, da
    except Exception as e:
        print(e)
        traceback.print_exc()
        return False, None


def parse_gpt_response_reformat(response):
    print(response)
    try:
        if '{' != response[0]:
            response = extract_bracket_content(response)
        da = json.loads(response.replace('\n', ''))

        assert isinstance(da["NaturalReasoning"], str), "NaturalReasoning should be str"
        assert '\n' in da["NaturalReasoning"], "NaturalReasoning should have \\n"
        return True, da
    except Exception as e:
        print(e)
        traceback.print_exc()
        return False, None


def get_stream_of_search(longcot):
    temp = '### {}\n{}\n'
    resstr = []
    for x in longcot:
        if 'title' in x:
            resstr.append(temp.format(x['title'], x['content']))
        else:
            resstr.append(temp.format(x['action'].replace('Final Conclusion', 'Conclusion'), x['content']))
    return '\n'.join(resstr).strip()


def filter_data(tmpdata):
    filtered_data = []
    for da in tmpdata:
        if 'Sentiment_instruction' not in da or 'Semantic_instruction' not in da or 'Style_instruction' not in da or 'Composite_instruction' not in da or 'Ground-True Answer' not in da:
            continue
        filtered_data.append(da)

    print(f"Original data size: {len(tmpdata)}, Filtered data size: {len(filtered_data)}")
    return filtered_data


def verify_gpt(conclusion, answer, d):
    query = verify_prompt.format(conclusion, answer)
    response = gpt_instance.retry_call(query)
    d['gpt4_query_cot'].append(query)
    d['gpt4_response_cot'].append(response)
    if 'true' in response.lower():
        d['verify'].append(True)
        return True
    else:
        d['verify'].append(False)
        return False


global wrongtime
wrongtime = 0


async def write_piece_order_data(d):
    global wrongtime
    try:
        retry_time = 1
        d['verify'] = []
        d['Long_CoT'] = []
        d['gpt4_query_cot'] = []
        d['gpt4_response_cot'] = []
        d['response_struct'] = []
        d['response_type'] = []
        d['prior_fail_try'] = []
        d['query_senti'] = []
        # d['reason_senti'] = []
        d['response_senti'] = []
        d['struct_senti'] = []
        d['query_semantic'] = []
        # d['reason_semantic'] = []
        d['response_semantic'] = []
        d['struct_semantic'] = []
        d['query_style'] = []
        # d['reason_style'] = []
        d['response_style'] = []
        d['struct_style'] = []
        d['response_type_subagent'] = []
        d['all_steps'] = []

        save_path = os.path.join(save_dir, str(d['process_id']) + ".json")


        response_senti, response_semantic, response_style, flag_senti, flag_semantic, flag_style = await (agents_initialreason(d)) # ok

        if not flag_senti or not flag_semantic or not flag_style:
            raise Exception('subagents init error')

        # Composite Agent prompt
        query_Composite = query_Composite_prompt_init.format(d['Composite_instruction'], response_senti, response_semantic, response_style) # initial prompt OK
        d['gpt4_query_cot'].append(query_Composite)
        for ii in range(retry_time):
            response = gpt_instance.retry_call(query_Composite) # get response from gpt OK
            if ii == 0:
                d['gpt4_response_cot'].append(response)
            flag, struct = parse_gpt_response(response) # identify if the format of answer is correct and format the answer
            if flag:
                d['response_struct'].append(struct["CoT"])
                d['Long_CoT'] = struct["CoT"]
                d['response_type'].append('Init_CoT')
                d['all_steps'].append('Composite_Init_CoT')
                break
            else:
                print(f'retrying Init_CoT', flush=True)
        if not flag:
            raise Exception('init error')

        verify_gpt(d['Long_CoT'][-2]['content'], d['Ground-True Answer'], d) # verify answer

        for rethinking_try_time in range(args.max_search_attempts):
            if rethinking_try_time > 0:
                # Archive the failed state
                del d['prior_fail_try']
                save_d['prior_fail_try'].append(d)
                # Replace with a new state
                d = save_d

            # Save the initial state
            save_d = copy.deepcopy(d)

            # Begin search
            for rethink_time in range(args.max_search_depth):
                if d['verify'][-1]:
                    break

                # judge if the subagents same conclusion and error
                if judge_if_agents_nochange_sameerror(d):
                    # double check three agents
                    # rethinking
                    # double check three agents
                    flag_senti, flag_semantic, flag_style = await (agents_double_check(d, "sameerror_rethinking")) # OK
                    if not flag_senti or not flag_semantic or not flag_style:
                        raise Exception('subagents sameerror subagent error')

                    # composite
                    reasoning = json.dumps(d['Long_CoT'][:-1], ensure_ascii=False, indent=2)
                    if judge_if_agents_nochange_sameerror(d):
                        strategy_name, strategy = random.choice(search_strategies)
                        query = strategy.format(d['Composite_instruction'], d['response_senti'][-1],
                                                d['response_semantic'][-1], d['response_style'][-1], reasoning) # OK

                    else:
                        strategy_name = "sameerrorafteragentdouble"
                        query = Composite_prompt_afteragentsdoublecheck.format(d['Composite_instruction'], d['response_senti'][-1], d['response_semantic'][-1], d['response_style'][-1], reasoning) ## OK
                    d['gpt4_query_cot'].append(query)
                    response = gpt_instance.retry_call(query)
                    flag, struct = parse_gpt_response(response)

                    if flag:
                        d['gpt4_response_cot'].append(response)
                        d['response_struct'].append(struct["CoT"])
                        d['Long_CoT'] = d['Long_CoT'][:-1] + struct["CoT"] # 拼起所有推理步骤
                        d['response_type'].append(f'Rethink_sameerror_%s_check'%strategy_name)
                        d['all_steps'].append("Composite_Rethink_sameerror_%s_check"%strategy_name)
                    if not flag:
                        raise Exception('Subagets same error compose rethink error')
                    verify_gpt(d['Long_CoT'][-2]['content'], d['Ground-True Answer'], d)

                    continue

                reasoning = json.dumps(d['Long_CoT'][:-1], ensure_ascii=False, indent=2) # 把Composite所有思维链都加进来，去掉最后的verification
                # Search strategy
                strategy_name, strategy = random.choice(search_strategies) # OK
                query = strategy.format(d['Composite_instruction'], d['response_senti'][-1], d['response_semantic'][-1], d['response_style'][-1], reasoning) # OK
                d['gpt4_query_cot'].append(query)

                for ii in range(retry_time):
                    response = gpt_instance.retry_call(query) # ok
                    flag, struct = parse_gpt_response(response)

                    if flag:
                        d['gpt4_response_cot'].append(response)
                        d['response_struct'].append(struct["CoT"])
                        d['Long_CoT'] = d['Long_CoT'][:-1] + struct["CoT"]
                        d['response_type'].append(f'Re_CoT_{strategy_name}')
                        d['all_steps'].append(f'Composite_Re_CoT_{strategy_name}')
                        break
                    else:
                        print(f'retrying strategy {strategy_name}', flush=True)
                if not flag:
                    raise Exception('back first compose rethink error')
                verify_gpt(d['Long_CoT'][-2]['content'], d['Ground-True Answer'], d)
                # if compose still false, subagents update
                if not d['verify'][-1]:
                    strategy_name_subagent, strategy_subagent = random.choice(search_strategies_subagents)
                    if strategy_name_subagent == "doublecheck":
                        flag_senti, flag_semantic, flag_style = await (agents_double_check(d)) # OK
                    elif strategy_name_subagent == "communication":
                        flag_senti, flag_semantic, flag_style = await (agents_communication(d)) # OK
                    else:
                        print("The strategy_name: %s is Error"%strategy_name_subagent)
                        exit()

                    if not flag_senti or not flag_semantic or not flag_style:
                        raise Exception('back subagents rethink error')

                    # composite
                    reasoning = json.dumps(d['Long_CoT'][:-1], ensure_ascii=False, indent=2)

                    if judge_if_agents_nochange_sameerror(d):
                        strategy_name, strategy = random.choice(search_strategies)
                        query = strategy.format(d['Composite_instruction'], d['response_senti'][-1],
                                                d['response_semantic'][-1], d['response_style'][-1], reasoning) # OK
                        d['gpt4_query_cot'].append(query)
                    else:
                        strategy_name = "aftersubagentsdoublecheck"
                        query = Composite_prompt_afteragentsdoublecheck.format(d['Composite_instruction'],
                                                                           d['response_senti'][-1],
                                                                           d['response_semantic'][-1],
                                                                           d['response_style'][-1], reasoning) # OK
                    d['gpt4_query_cot'].append(query)
                    response = gpt_instance.retry_call(query)
                    flag, struct = parse_gpt_response(response)

                    if flag:
                        d['gpt4_response_cot'].append(response)
                        d['response_struct'].append(struct["CoT"])
                        d['Long_CoT'] = d['Long_CoT'][:-1] + struct["CoT"]  # 拼起所有推理步骤
                        d['response_type'].append(f'Rethink_1compose2subagent_%s_check'%strategy_name)
                        d['all_steps'].append(f'Composite_Rethink_1compose2subagent_%s_check'%strategy_name)
                    if not flag:
                        raise Exception('back after subagents compose rethink error')
                    verify_gpt(d['Long_CoT'][-2]['content'], d['Ground-True Answer'], d)

            if d['verify'][-1]:
                break

        # If it is still incorrect, give a hint
        if not d['verify'][-1] and args.efficient_search: ###

            flag_senti, flag_semantic, flag_style = await (agents_gen_with_label(d))
            if not flag_senti or not flag_semantic or not flag_style:
                raise Exception('subagents Label_CoT error')

            reasoning = json.dumps(d['Long_CoT'][:-1], ensure_ascii=False, indent=2)
            query = gen_prompt_w_label.format(d['Composite_instruction'],
                                              d['response_senti'][-1],
                                              d['response_semantic'][-1],
                                              d['response_style'][-1],reasoning,
                                              d['Ground-True Answer'])
            d['gpt4_query_cot'].append(query)
            for ii in range(retry_time):
                response = gpt_instance.retry_call(query)
                flag, struct = parse_gpt_response(response)
                if flag:
                    d['gpt4_response_cot'].append(response)
                    d['response_struct'].append(struct["CoT"])
                    d['Long_CoT'] = d['Long_CoT'][:-1] + struct["CoT"]
                    d['response_type'].append('Label_CoT')
                    d['all_steps'].append('Composite_Label_CoT')
                    # ignore verify
                    d['verify'].append(True)
                    break
                else:
                    print(f'retrying Label_CoT', flush=True)
            if not flag:
                raise Exception('label error')

        if d['verify'][-1]:
            # Generate complex CoT and final response (Complex_CoT, response)
            sos = get_stream_of_search(d['Long_CoT'])
            query = reformat_to_complex_cot_prompt.format(sos, d['Composite_instruction'])
            d['gpt4_query_cot'].append(query)
            for ii in range(retry_time):
                response = gpt_instance.retry_call(query)
                flag, struct = parse_gpt_response_reformat(response)
                if flag:
                    d['gpt4_response_cot'].append(response)
                    d["Complex_CoT"] = struct["NaturalReasoning"]
                    # get response
                    query = get_final_response_prompt.format(d['Complex_CoT'], d['Composite_instruction']) # ok
                    d['gpt4_query_cot'].append(query)
                    response = gpt_instance.retry_call(query)
                    d['gpt4_response_cot'].append(response)
                    d["Response"] = response
                    d['Question'] = d['Composite_instruction']
                    break

        with open(save_path, mode="w", encoding="utf-8") as fw:
            json.dump(d, fw, ensure_ascii=False, indent=2)
            wrongtime = 0

    except Exception as e:
        traceback.print_exc()
        wrongtime += 1
        if wrongtime > 20:
            assert 1 == 0, 'wrong'
    return 1


def deduplicate_data(data, processed_data):
    processed_ids = {item['Index'] for item in processed_data}
    return [item for item in data if item['Index'] not in processed_ids]


def merge_saved_files(save_dir):
    _, _, filenames = [i for i in os.walk(save_dir)][0]
    json_files = [f for f in filenames if f.endswith('.json')]
    res = []
    for file_path in json_files:
        try:
            with open(os.path.join(save_dir, file_path), encoding="utf-8") as f:
                da = json.loads(f.read())
                assert 'Complex_CoT' in da and 'Response' in da
                res.append(da)
        except Exception as e:
            continue
    return res


async def main(input_data):
    import asyncio
    from tqdm.asyncio import tqdm_asyncio

    sem = asyncio.Semaphore(5)

    async def sem_task(item):
        async with sem:
            return await write_piece_order_data(item)

    results = await tqdm_asyncio.gather(
        *[sem_task(item) for item in input_data],
        total=len(input_data)
    )


    # Merge and save final output
    final_data = merge_saved_files(save_dir)
    output_path = f"../data/{task_name}.json"
    print(f"Processed {len(final_data)} items. Saving to {output_path}")

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(final_data, file, ensure_ascii=False, indent=2)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default='AMTCele')
    parser.add_argument("--max_search_attempts", type=int, default=1, help="Maximum number of search attempts.")
    parser.add_argument("--max_search_depth", type=int, default=2, help="Maximum search depth.")
    parser.add_argument("--efficient_search", type=bool, default=True, help="Enable efficient search strategy.")
    parser.add_argument("--num_process", type=int, default=5, help="Number of parallel processes.")

    parser.add_argument("--limit_num", type=int, default=5, help="Limit the number of processed items.")
    # parser.add_argument("--limit_num", type=int, help="Limit the number of processed items.")

    args = parser.parse_args()

    tmpdata = load_dataset("json", data_files={"train": "./retrievaldata/"+args.dataset+"_all_train_for_cot.json"})


    tmpdata = tmpdata["train"]
    tmpdata = [
        {
            "Sentiment_instruction": record["Sentiment_instruction"],
            "Semantic_instruction": record["Semantic_instruction"],
            "Style_instruction": record["Style_instruction"],
            "Composite_instruction": record["Composite_instruction"],
            "Ground-True Answer": record["Ground-True Answer"],
            "Instruction": record["Instruction"],
            "Short_Answer": record['Short_Answer'],
            "Index": record["index"],
        }
        for record in tmpdata
    ]

    tmp_id = 1
    for da in tmpdata:
        da['process_id'] = da["Index"]
        tmp_id += 1
    data = filter_data(tmpdata)


    print(f"read data:{len(data)}")


    task_name = f'{args.dataset}_RL_with_CoT'
    save_dir = f'output_data/{task_name}'

    gpt_instance = DeepSeek("deepseek-chat")

    os.makedirs(save_dir, exist_ok=True)

    # Merge previously processed files
    processed_data = merge_saved_files(save_dir)
    print(f"Previously processed items: {len(processed_data)}")

    input_data = deduplicate_data(data, processed_data)
    print(f"Items remaining for processing: {len(input_data)}")

    asyncio.run(main(input_data))
