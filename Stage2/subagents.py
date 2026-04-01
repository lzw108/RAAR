import re
import traceback
from call_llm import *

import asyncio
# from tinyagent import TinyAgent
# from tinyagent.storage.sqlite_storage import SqliteStorage

from openai import AsyncOpenAI


from cot_prompt_en import verify_prompt, search_strategies, \
    query_Sentiment_prompt_init, query_Semantic_prompt_init, query_Style_prompt_init, Sentiment_rethinking_doublecheck, \
    Semantic_rethinking_doublecheck, Style_rethinking_doublecheck, \
    Sentiment_rethinking_communication, Semantic_rethinking_communication, Style_rethinking_communication, \
    Sentiment_rethinking_withlabel, Semantic_rethinking_withlabel, Style_rethinking_withlabel

api_key = ""
base_url = "https://api.deepseek.com"
model_version = "deepseek-chat"

async def async_query_openai(query, additional_args=None):
    if additional_args is None:
        additional_args = {}

    messages = [{'role': 'user', 'content': query}]

    # aclient = AsyncOpenAI(
    #         api_key=ali_key,
    #         base_url=ali_url,
    #     )




    # completion = await aclient.chat.completions.create(
    #     model=model_version,
    #     messages=messages,
    #     extra_body={"enable_thinking": False},  # deepseek 兼容模式参数
    #     # extra_body={
    #     #     "thinking": {
    #     #         "type": "enabled"
    #     #     }},
    #     max_completion_tokens=8192,
    #     temperature=1
    # )

    # official Deepseek
    aclient = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    completion = await aclient.chat.completions.create(
        model=model_version,
        messages=messages,
        max_completion_tokens=8192,
        temperature=1
    )

    answer = completion.choices[0].message.content
    if answer.strip() == "broken":
        return await async_query_openai(query, additional_args)
    return answer

# class MultiAgents:
#     def __init__(self, api_key):
#         self.api_key = deepseek_key
#
#     async def init(self):
#         self.agent_sentiment = await TinyAgent.create(
#             model=model_version,
#             api_key=self.api_key,
#             system_prompt="You are a helpful sentiment analysis expert",
#             session_id="chat-session-sentiment",
#             user_id="user-alice",
#             metadata={"user_name": "agent_sentiment", "role": "sentiment expert"}
#         )
#
#         self.agent_semantic = await TinyAgent.create(
#             model=model_version,
#             api_key=self.api_key,
#             system_prompt="You are a helpful semantic analysis expert",
#             session_id="chat-session-semantic",
#             user_id="user-bob",
#             metadata={"user_name": "agent_semantic", "role": "semantic expert"}
#         )
#
#         self.agent_style = await TinyAgent.create(
#             model=model_version,
#             api_key=self.api_key,
#             system_prompt="You are a helpful writing style analysis expert",
#             session_id="chat-session-style",
#             user_id="user-bob",
#             metadata={"user_name": "agent_style", "role": "writing style expert"}
#         )
#
#     async def close(self):
#         await self.agent_sentiment.close()
#         await self.agent_semantic.close()
#         await self.agent_style.close()
#
#     async def sentiment(self, text):
#         print("Sentiment agent is thinking:")
#         response = await self.agent_sentiment.run(text)
#         if response == "Task completed without final answer.!!!" or response.strip() == "":
#             print("Sentiment agent: retrying")
#             response = await self.agent_sentiment.run(text)
#         print("Sentiment agent: ", response)
#         return response
#
#     async def semantic(self, text):
#         print("Semantic agent is thinking:")
#         response = await self.agent_semantic.run(text)
#         if response == "Task completed without final answer.!!!" or response.strip() == "":
#             print("Semantic agent: retrying")
#             response = await self.agent_semantic.run(text)
#         print("Semantic agent: ", response)
#         return response
#
#     async def style(self, text):
#         print("Style agent is thinking:")
#         response = await self.agent_style.run(text)
#         if response == "Task completed without final answer.!!!" or response.strip() == "":
#             response = await self.agent_style.run(text)
#             print("Style agent: retrying")
#         print("Style agent: ", response)
#         return response

def extract_bracket_content(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    start = text.find('{')
    return text[start:] if start != -1 else None

def parse_gpt_response_agents(response):
    try:
        if '{' != response.strip()[0]:
            response = extract_bracket_content(response)
        open_count = response.count('{')
        close_count = response.count('}')
        if open_count > close_count:
            response += '}' * (open_count - close_count)
        da = json.loads(response.replace('\n', '').replace("```", ''))
        # assert isinstance(da["response"], list), "should be list"
        keys = list(da.keys())
        assert keys[0] == "judgment", "should include judgment" # first key
        assert keys[1] == "reason", "should include reason" # second key
        response = f"judgment: {da['judgment']}\nreason: {da['reason']}"
        return True, da, response
    except Exception as e:
        print(e)
        traceback.print_exc()
        return False, None

# Initial agents reasoning
async def agents_initialreason(d):
    # generate initial reasoning of subagents
    # agents = MultiAgents(openai_key)
    # await agents.init()

    print("agents are initing.")

    query_senti = query_Sentiment_prompt_init.format(d['Sentiment_instruction'])
    query_semantic = query_Semantic_prompt_init.format(d['Semantic_instruction'])
    query_style = query_Style_prompt_init.format(d['Style_instruction'])

    # try:
    #     responsegpt_senti, responsegpt_semantic, responsegpt_style = await asyncio.gather(
    #         agents.sentiment(query_senti),
    #         agents.semantic(query_semantic),
    #         agents.style(query_style)
    #     )
    # finally:
    #     # pass
    #     await agents.close()
    queries = [query_senti, query_semantic, query_style]
    responsegpt_senti, responsegpt_semantic, responsegpt_style = await asyncio.gather(*(async_query_openai(query) for query in queries))
    print("Sentiment agent: ", responsegpt_senti)
    print("Semantic agent: ", responsegpt_semantic)
    print("Style agent: ", responsegpt_style)

    flag_senti, struct_senti, response_senti = parse_gpt_response_agents(responsegpt_senti)
    d['struct_senti'].append(struct_senti)
    d['query_senti'].append(query_senti)
    d['response_senti'].append(response_senti)

    # semantic agent
    flag_semantic, struct_semantic, response_semantic = parse_gpt_response_agents(responsegpt_semantic)
    d['struct_semantic'].append(struct_semantic)
    d['query_semantic'].append(query_semantic)
    d['response_semantic'].append(response_semantic)

    # writing agent
    flag_style, struct_style, response_style = parse_gpt_response_agents(responsegpt_style)
    d['struct_style'].append(struct_style)
    d['query_style'].append(query_style)
    d['response_style'].append(response_style)

    d['response_type_subagent'].append("Init")
    d['all_steps'].append("subagents_init")

    return response_senti, response_semantic, response_style, flag_senti, flag_semantic, flag_style

def judge_if_agents_nochange_sameerror(d):

    # 判断subagents结果是否一样并且错误
    if d['struct_senti'][-1]["judgment"].lower().strip() == d['struct_semantic'][-1][ \
            "judgment"].lower().strip() == d['struct_style'][-1]["judgment"].lower().strip() and \
            d['struct_style'][-1]["judgment"].lower().strip() != d["Short_Answer"].lower().strip():
        return True
    # 判断subagents结果和上一次是否相同
    elif len(d['struct_senti']) > 1 and len(d['struct_semantic']) > 1 and len(d['struct_style']) > 1:
        if d['struct_senti'][-1]["judgment"].lower().strip() == d['struct_senti'][-2]["judgment"].lower().strip() and \
            d['struct_semantic'][-1]["judgment"].lower().strip() == d['struct_semantic'][-2]["judgment"].lower().strip() and \
            d['struct_style'][-1]["judgment"].lower().strip() == d['struct_style'][-2]["judgment"].lower().strip():
            return True
        else:
            return False
    else:
        return False

async def agents_double_check(d, rethink_name="agents_double_check"):

    # agents = MultiAgents(openai_key)
    # await agents.init()

    previous_senti = json.dumps(d['struct_senti'], ensure_ascii=False, indent=2)
    query_senti = Sentiment_rethinking_doublecheck.format(d['Sentiment_instruction'], previous_senti)
    previous_semantic = json.dumps(d['struct_semantic'], ensure_ascii=False, indent=2)
    query_semantic = Semantic_rethinking_doublecheck.format(d['Semantic_instruction'], previous_semantic)
    previous_style = json.dumps(d['struct_style'], ensure_ascii=False, indent=2)
    query_style = Style_rethinking_doublecheck.format(d['Style_instruction'], previous_style)

    queries = [query_senti, query_semantic, query_style]
    responsegpt_senti, responsegpt_semantic, responsegpt_style = await asyncio.gather(
        *(async_query_openai(query) for query in queries))
    print("Sentiment agent: ", responsegpt_senti)
    print("Semantic agent: ", responsegpt_semantic)
    print("Style agent: ", responsegpt_style)

    flag_senti, struct_senti, response_senti = parse_gpt_response_agents(responsegpt_senti)
    d['struct_senti'].append(struct_senti)
    d['response_senti'].append(response_senti)
    d['query_senti'].append(query_senti)

    flag_semantic, struct_semantic, response_semantic = parse_gpt_response_agents(responsegpt_semantic)
    d['struct_semantic'].append(struct_semantic)
    d['response_semantic'].append(response_semantic)
    d['query_semantic'].append(query_semantic)

    flag_style, struct_style, response_style = parse_gpt_response_agents(responsegpt_style)
    d['struct_style'].append(struct_style)
    d['response_style'].append(response_style)
    d['query_style'].append(query_style)

    d['response_type_subagent'].append(rethink_name)
    d['all_steps'].append(rethink_name)

    return flag_senti, flag_semantic, flag_style


async def agents_communication(d, rethink_name="agents_communication"):

    # agents = MultiAgents(openai_key)
    # await agents.init()

    previous_senti = json.dumps(d['struct_senti'], ensure_ascii=False, indent=2)
    previous_semantic = json.dumps(d['struct_semantic'], ensure_ascii=False, indent=2)
    previous_style = json.dumps(d['struct_style'], ensure_ascii=False, indent=2)

    query_senti = Sentiment_rethinking_communication.format(d['Sentiment_instruction'], previous_senti,
                                                            d["Semantic_instruction"] + previous_semantic,
                                                            d["Style_instruction"] + previous_style)
    query_semantic = Semantic_rethinking_communication.format(d['Semantic_instruction'], previous_semantic,
                                                              d["Sentiment_instruction"] + previous_senti,
                                                              d["Style_instruction"] + previous_style)
    query_style = Style_rethinking_communication.format(d['Style_instruction'], previous_style,
                                                        d["Sentiment_instruction"] + previous_senti,
                                                        d["Semantic_instruction"] + previous_semantic)

    queries = [query_senti, query_semantic, query_style]
    responsegpt_senti, responsegpt_semantic, responsegpt_style = await asyncio.gather(
        *(async_query_openai(query) for query in queries))
    print("Sentiment agent: ", responsegpt_senti)
    print("Semantic agent: ", responsegpt_semantic)
    print("Style agent: ", responsegpt_style)

    flag_senti, struct_senti, response_senti = parse_gpt_response_agents(responsegpt_senti)
    d['struct_senti'].append(struct_senti)
    d['response_senti'].append(response_senti)
    d['query_senti'].append(query_senti)

    flag_semantic, struct_semantic, response_semantic = parse_gpt_response_agents(responsegpt_semantic)
    d['struct_semantic'].append(struct_semantic)
    d['response_semantic'].append(response_semantic)
    d['query_semantic'].append(query_semantic)

    flag_style, struct_style, response_style = parse_gpt_response_agents(responsegpt_style)
    d['struct_style'].append(struct_style)
    d['response_style'].append(response_style)
    d['query_style'].append(query_style)

    d['response_type_subagent'].append(rethink_name)
    d['all_steps'].append(rethink_name)

    return flag_senti, flag_semantic, flag_style

async def agents_gen_with_label(d):



    flag_senti, flag_semantic, flag_style = True, True, True

    # agents = MultiAgents(openai_key)
    # await agents.init()


    queries = []
    if d['struct_senti'][-1]["judgment"].lower().strip() != d["Short_Answer"].lower().strip():
        previous_senti = json.dumps(d['struct_senti'], ensure_ascii=False, indent=2)
        query_senti = Sentiment_rethinking_withlabel.format(d['Sentiment_instruction'], previous_senti,
                                                            d['Ground-True Answer'])
        queries.append(("senti", query_senti))

    if d['struct_semantic'][-1]["judgment"].lower().strip() != d["Short_Answer"].lower().strip():
        previous_semantic = json.dumps(d['struct_semantic'], ensure_ascii=False, indent=2)
        query_semantic = Semantic_rethinking_withlabel.format(d['Semantic_instruction'], previous_semantic,
                                                              d['Ground-True Answer'])
        queries.append(("semantic", query_semantic))

    if d['struct_style'][-1]["judgment"].lower().strip() != d["Short_Answer"].lower().strip():
        previous_style = json.dumps(d['struct_style'], ensure_ascii=False, indent=2)
        query_style = Style_rethinking_withlabel.format(d['Style_instruction'], previous_style, d['Ground-True Answer'])
        queries.append(("style", query_style))

    # queries = [query_senti, query_semantic, query_style]
    results = await asyncio.gather(
        *(async_query_openai(query) for name, query in queries))


    for (name, query), response in zip(queries, results):
        if name == "senti":
            print("Sentiment agent: ", response)
            flag_senti, struct_senti, response_senti = parse_gpt_response_agents(response)
            d['struct_senti'].append(struct_senti)
            d['response_senti'].append(response_senti)
            d['query_senti'].append(query_senti)

        elif name == "semantic":
            print("Semantic agent: ", response)
            flag_semantic, struct_semantic, response_semantic = parse_gpt_response_agents(response)
            d['struct_semantic'].append(struct_semantic)
            d['response_semantic'].append(response_semantic)
            d['query_semantic'].append(query_semantic)

        elif name == "style":
            print("Style agent: ", response)
            flag_style, struct_style, response_style = parse_gpt_response_agents(response)
            d['struct_style'].append(struct_style)
            d['response_style'].append(response_style)
            d['query_style'].append(query_style)

    names = [name for name, query in queries]
    if "senti" not in names:
        print("The last step of Sentiment agent is correct. Copy from last step.")
        d['struct_senti'].append(d['struct_senti'][-1])
        d['response_senti'].append(d['response_senti'][-1])
        d['query_senti'].append(d['response_senti'][-1])
    if "semantic" not in names:
        print("The last step of Semantic agent is correct. Copy from last step.")
        d['struct_semantic'].append(d['struct_semantic'][-1])
        d['response_semantic'].append(d['response_semantic'][-1])
        d['query_semantic'].append(d['query_semantic'][-1])
    if "style" not in names:
        print("The last step of Style agent is correct. Copy from last step.")
        d['struct_style'].append(d['struct_style'][-1])
        d['response_style'].append(d['response_style'][-1])
        d['query_style'].append(d['query_style'][-1])

    d['response_type_subagent'].append("rethinking_withlabel")
    d['all_steps'].append("rethinking_withlabel")

    return flag_senti, flag_semantic, flag_style

