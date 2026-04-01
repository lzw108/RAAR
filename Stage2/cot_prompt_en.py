verify_prompt = """<Model Response>  
{}  
</Model Response>  

<Reference Answer>  
{}
</Reference Answer>  

You are provided with a model-generated response (<Model Response>) and a reference answer (<Reference Answer>). Compare the model response with the reference answer and determine its correctness. Your task is to simply output "True" if the response is correct, and "False" otherwise."""


query_Sentiment_prompt_init = """<question>
{}
</question>

You are an expert in sentiment analysis. You need to collaborate with a semantic analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the sentiment analysis component. Respond to the question from the perspective of sentiment analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Sentiment_rethinking_doublecheck = """<question>
{}
</question>

<previous response>
{}
</previous response>

<response requirements>

You are an expert in sentiment analysis. You need to collaborate with a semantic analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the sentiment analysis component. Respond to the question from the perspective of sentiment analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. An overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. Please double-check your answer. If you still stand by your judgment, provide additional evidence. If you find an issue, provide a revised judgment along with your reasoning.

### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Sentiment_rethinking_communication = """<question>
{}
</question>

<previous response>
{}
</previous response>

<semantic agent>
{}
</semantic agent>

<style agent>
{}
</style agent>

<response requirements>

You are an expert in sentiment analysis. You need to collaborate with a semantic analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the sentiment analysis component. Respond to the question from the perspective of sentiment analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. <semantic agent> and <style agent> are the corresponding examples and analysis from a semantic analysis expert and a writing style analysis expert. In the last round, an overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. At this communication stage, please double-check your answer and consider the feedback from the other experts. If you still stand by your judgment, provide additional evidence. If you find an issue, provide a revised judgment along with your reasoning.
### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Sentiment_rethinking_withlabel = """<question>
{}
</question>

<previous response>
{}
</previous response>

<response requirements>

You are an expert in sentiment analysis. You need to collaborate with a semantic analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the sentiment analysis component. Respond to the question from the perspective of sentiment analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. An overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. Now, I'll secretly tell you that the labeled answer is "{}", but you must pretend not to know. Please refine your answer accordingly to ensure the final answer aligns with the correct one.

### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

query_Semantic_prompt_init = """<question>
{}
</question>

You are an expert in semantic analysis. You need to collaborate with a sentiment analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the semantic analysis component. Respond to the question from the perspective of semantic analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Semantic_rethinking_doublecheck = """<question>
{}
</question>

<previous response>
{}
</previous response>

<response requirements>

You are an expert in semantic analysis. You need to collaborate with a sentiment analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the semantic analysis component. Respond to the question from the perspective of semantic analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. An overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. Please double-check your answer. If you still stand by your judgment, provide additional evidence. If you find an issue, provide a revised judgment along with your reasoning.

### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Semantic_rethinking_communication = """<question>
{}
</question>

<previous response>
{}
</previous response>

<sentiment agent>
{}
</sentiment agent>

<style agent>
{}
</style agent>

<response requirements>

You are an expert in semantic analysis. You need to collaborate with a sentiment analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the semantic analysis component. Respond to the question from the perspective of semantic analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. <sentiment agent> and <style agent> are the corresponding examples and analysis from a sentiment analysis expert and a writing style analysis expert. In the last round, an overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. At this communication stage, please double-check your answer and consider the feedback from the other experts. If you still stand by your judgment, provide additional evidence. If you find an issue, provide a revised judgment along with your reasoning.

### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Semantic_rethinking_withlabel = """<question>
{}
</question>

<previous response>
{}
</previous response>

<response requirements>

You are an expert in semantic analysis. You need to collaborate with a sentiment analysis expert and a writing style analysis expert to address the above problem. Your primary responsibility is the semantic analysis component. Respond to the question from the perspective of semantic analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. An overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. Now, I'll secretly tell you that the labeled answer is "{}", but you must pretend not to know. Please refine your answer accordingly to ensure the final answer aligns with the correct one.

### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""


query_Style_prompt_init = """<question>
{}
</question>

You are an expert in writing style analysis. You need to collaborate with a sentiment analysis expert and a semantic analysis expert to address the above problem. Your primary responsibility is the writing style analysis component. Respond to the question from the perspective of writing style analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Style_rethinking_doublecheck = """<question>
{}
</question>

<previous response>
{}
</previous response>

<response requirements>

You are an expert in writing style analysis. You need to collaborate with a sentiment analysis expert and a semantic analysis expert to address the above problem. Your primary responsibility is the writing style analysis component. Respond to the question from the perspective of writing style analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. An overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. Please double-check your answer. If you still stand by your judgment, provide additional evidence. If you find an issue, provide a revised judgment along with your reasoning.


### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Style_rethinking_communication = """<question>
{}
</question>

<previous response>
{}
</previous response>

<sentiment agent>
{}
</sentiment agent>

<semantic agent>
{}
</semantic agent>


<response requirements>

You are an expert in writing style analysis. You need to collaborate with a sentiment analysis expert and a semantic analysis expert to address the above problem. Your primary responsibility is the writing style analysis component. Respond to the question from the perspective of writing style analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. <sentiment agent> and <semantic agent> are the corresponding examples and analysis from a sentiment analysis expert and a semantic analysis expert. In the last round, an overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. At this communication stage, please double-check your answer and consider the feedback from the other experts. If you still stand by your judgment, provide additional evidence. If you find an issue, provide a revised judgment along with your reasoning.

### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""

Style_rethinking_withlabel = """<question>
{}
</question>

<previous response>
{}
</previous response>

<response requirements>

You are an expert in writing style analysis. You need to collaborate with a sentiment analysis expert and a semantic analysis expert to address the above problem. Your primary responsibility is the writing style analysis component. Respond to the question from the perspective of writing style analysis, incorporating retrieved examples. Provide your judgment along with well-reasoned evidence or explanations.
You must provide a specific answer that fully aligns with the task description. 

</response requirements>

<question> represents the question to be answered, and <previous response> contains your prior answer. An overseeing expert has integrated the opinions of your three experts, but the final answer is incorrect. Now, I'll secretly tell you that the labeled answer is "{}", but you must pretend not to know. Please refine your answer accordingly to ensure the final answer aligns with the correct one.

### Output Format
The output format must strictly follow the JSON structure below:
```json
{{
  "judgment": "...", "reason": "..."
}}
```"""


query_Composite_prompt_init = """<question>
{}
</question>

<sentiment>
{}
</sentiment>

<semantic>
{}
</semantic>

<style>
{}
</style>

Please respond to the above question <question> using the Chain of Thought (CoT) reasoning method. During the reasoning process, please consider information from the three expert agents. <sentiment> denotes analysis based on sentiment and examples retrieved by sentiment intensity. <semantic> denotes analysis based on semantics and examples retrieved by semantic information. <style> denotes analysis based on writing style and examples retrieved by writing style. And you may also incorporate your own independent reasoning.
Your response should consist of multiple steps, each of which includes three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

- **'Inner Thinking'**: This is the step where thinking is done. Note that multiple 'Inner Thinking' steps are required to describe thorough reasoning. Each step should first generate a brief title.
- **'Final Conclusion'**: At this stage, you summarize the correct reasoning from previous 'Inner Thinking' steps and provide the final answer. No title is required here.
- **'Verification'**: At this stage, you verify the conclusion from the "Final Conclusion" step. If the conclusion holds, end the process. If not, return to "Inner Thinking" for further reasoning. No title is required here.

The output format must strictly follow the JSON structure below:
```json
{{
"CoT": [
    {{"action": "Inner Thinking", "title": "...", "content": "..."}},
    ...,
    {{"action": "Final Conclusion", "content": "..."}},
    {{"action": "Verification", "content": "..."}}
]
}}
```"""

Composite_prompt_afteragentsdoublecheck = """<question>
{}
</question>

<sentiment>
{}
</sentiment>

<semantic>
{}
</semantic>

<style>
{}
</style>

<previous reasoning>
{}
</previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, <sentiment>, <semantic>, and <style> are derived from the latest analyses of three experts, each from a different perspective, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. Upon review, your previous reasoning and Final Conclusion appear incomplete or insufficiently justified or false. Proceed to refine the reasoning based on the three experts’ latest analysis in <sentiment>, <semantic>, and <style> and construct a new Final Conclusion. And you may also incorporate your own independent reasoning.

### Output Format
Strictly follow the JSON structure below. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.
```json
{{
"CoT": [
    {{"action": "Verification", "content": "..."}},
    {{"action": "Inner Thinking", "title": "...", "content": "..."}},
    ...,
    {{"action": "Final Conclusion", "content": "..."}},
    {{"action": "Verification", "content": "..."}}
]
}}
```"""



gen_prompt_rethink_Backtracking = """<question>
{}
</question>

<sentiment>
{}
</sentiment>

<semantic>
{}
</semantic>

<style>
{}
</style>

<previous reasoning>
{}
</previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, <sentiment>, <semantic>, and <style> are derived from the latest analyses of three experts, each from a different perspective, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. Upon review, your previous reasoning and Final Conclusion appear incomplete or insufficiently justified or false. Proceed to refine the reasoning using **backtracking** to revisit earlier points of reasoning and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
    {{"action": "Verification", "content": "..."}},
    {{"action": "Inner Thinking", "title": "...", "content": "..."}},
    ...,
    {{"action": "Final Conclusion", "content": "..."}},
    {{"action": "Verification", "content": "..."}}
]
}}
```"""

gen_prompt_rethink_Exploring_New_Path = """<question>
{}
</question>

<sentiment>
{}
</sentiment>

<semantic>
{}
</semantic>

<style>
{}
</style>

<previous reasoning>
{}
</previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, <sentiment>, <semantic>, and <style> are derived from the latest analyses of three experts, each from a different perspective, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. Upon review, your previous reasoning and Final Conclusion appear incomplete or insufficiently justified or false. Proceed to refine the reasoning by exploring new approaches to solving this problem and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
    {{"action": "Verification", "content": "..."}},
    {{"action": "Inner Thinking", "title": "...", "content": "..."}},
    ...,
    {{"action": "Final Conclusion", "content": "..."}},
    {{"action": "Verification", "content": "..."}}
]
}}
```"""

gen_prompt_rethink_Verification = """<question>
{}
</question>

<sentiment>
{}
</sentiment>

<semantic>
{}
</semantic>

<style>
{}
</style>

<previous reasoning>
{}
</previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, <sentiment>, <semantic>, and <style> are derived from the latest analyses of three experts, each from a different perspective, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. Upon review, your previous reasoning and Final Conclusion appear incomplete or insufficiently justified or false. Proceed to refine the reasoning by conducting a thorough **validation** process to ensure validity and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
    {{"action": "Verification", "content": "..."}},
    {{"action": "Inner Thinking", "title": "...", "content": "..."}},
    ...,
    {{"action": "Final Conclusion", "content": "..."}},
    {{"action": "Verification", "content": "..."}}
]
}}
```"""

gen_prompt_rethink_Correction = """<question>
{}
</question>

<sentiment>
{}
</sentiment>

<semantic>
{}
</semantic>

<style>
{}
</style>

<previous reasoning>
{}
</previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, <sentiment>, <semantic>, and <style> are derived from the latest analyses of three experts, each from a different perspective, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. Upon review, your previous reasoning and Final Conclusion appear incomplete or insufficiently justified or false. Proceed to refine the reasoning by making precise **corrections** to address prior flaws and construct a new Final Conclusion.

### Output Format
Strictly follow the JSON structure below. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
    {{"action": "Verification", "content": "..."}},
    {{"action": "Inner Thinking", "title": "...", "content": "..."}},
    ...,
    {{"action": "Final Conclusion", "content": "..."}},
    {{"action": "Verification", "content": "..."}}
]
}}
```"""

gen_prompt_w_label = """<question>
{}
</question>

<sentiment>
{}
</sentiment>

<semantic>
{}
</semantic>

<style>
{}
</style>

<previous reasoning>
{}
</previous reasoning>

<response requirements>
Your response must include the following steps, each composed of three types of actions: **"Inner Thinking"**, **"Final Conclusion"**, and **"Verification"**:

1. **Inner Thinking**: Break down the reasoning process into multiple concise steps. Each step should start with a brief title to clarify its purpose.
2. **Final Conclusion**: Summarize the correct reasoning from all previous 'Inner Thinking' steps and provide the final answer. No title is needed for this section.
3. **Verification**: Verify the accuracy of the "Final Conclusion". If it holds, conclude the process. Otherwise, return to "Inner Thinking" for further refinement.

</response requirements>

<question> represents the question to be answered, <sentiment>, <semantic>, and <style> are derived from the latest analyses of three experts, each from a different perspective, and <previous reasoning> contains your prior reasoning. Your task is to continue from the current 'Verification' step. Now, I'll secretly tell you that the labeled answer is "{}", but you must pretend not to know. Your 'Verification' requires careful consideration, and if incorrect, you need to provide new Inner Thinking steps and a new Final Conclusion to ensure the final answer aligns with the correct one.

### Output Format
Strictly follow the JSON structure below. You do not need to repeat your previous reasoning. Begin directly from the next 'Verification' stage.

```json
{{
"CoT": [
    {{"action": "Verification", "content": "..."}},
    {{"action": "Inner Thinking", "title": "...", "content": "..."}},
    ...,
    {{"action": "Final Conclusion", "content": "..."}},
    {{"action": "Verification", "content": "..."}}
]
}}
```"""

reformat_to_complex_cot_prompt = """<Thought Process>
{}
</Thought Process>

<Question>
{}
</Question>

The <Thought Process> above reflects the model's reasoning based on the <Question>. Your task is to rewrite the <Thought Process> to resemble a more human-like, intuitive natural thinking process. The new version should:

1. Be presented as step-by-step reasoning, with each thought on a new line separated by a line break.
2. Avoid structured titles or formatting, focusing on natural transitions. Use casual and natural language for transitions or validations, such as "hmm," "oh," "also," or "wait."
3. Expand the content, making the reasoning richer, more detailed, and logically clear while still being conversational and intuitive.
4. Avoid phrasing it as something an agent said, transforming it into your own thinking.

Return directly the revised natural thinking in JSON format as follows:
```json
{{
  "NaturalReasoning": "..."
}}
```"""

reformat_to_complex_cot_prompt_highlight = """<Thought Process>
{}
</Thought Process>

<Question>
{}
</Question>

The <Thought Process> above reflects the model's reasoning based on the <Question> (Please note that only the last "### Conclusion" in <Thought Process> is the final correct answer. Please answer strictly according to the last answer marked as "### Conclusion" in <Thought Process>; the others are merely part of the reasoning process). Your task is to rewrite the <Thought Process> to resemble a more human-like, intuitive natural thinking process. The new version should:

1. Be presented as step-by-step reasoning, with each thought on a new line separated by a line break.
2. Avoid structured titles or formatting, focusing on natural transitions. Use casual and natural language for transitions or validations, such as "hmm," "oh," "also," or "wait."
3. Expand the content, making the reasoning richer, more detailed, and logically clear while still being conversational and intuitive.
4. Avoid phrasing it as something an agent said, transforming it into your own thinking.

Return directly the revised natural thinking in JSON format as follows:
```json
{{
  "NaturalReasoning": "..."
}}
```"""


reformat_to_complex_cot_prompt_highlight_withlabel = """<Thought Process>
{}
</Thought Process>

<Question>
{}
</Question>

The <Thought Process> above reflects the model's reasoning based on the <Question> (Please note that only the last "### Conclusion" in <Thought Process> is the final correct answer. Please answer strictly according to the last answer marked as "### Conclusion" in <Thought Process>; I'll secretly tell you that the labeled answer is "{}"). Your task is to rewrite the <Thought Process> to resemble a more human-like, intuitive natural thinking process. The new version should:

1. Be presented as step-by-step reasoning, with each thought on a new line separated by a line break.
2. Avoid structured titles or formatting, focusing on natural transitions. Use casual and natural language for transitions or validations, such as "hmm," "oh," "also," or "wait."
3. Expand the content, making the reasoning richer, more detailed, and logically clear while still being conversational and intuitive.
4. Avoid phrasing it as something an agent said, transforming it into your own thinking.

Return directly the revised natural thinking in JSON format as follows:
```json
{{
  "NaturalReasoning": "..."
}}
```"""

get_final_response_prompt = """<Internal Thinking>
{}
</Internal Thinking>

<Question>
{}
</Question>

The <Internal Thinking> represents your internal thoughts about the <Question>. Based on this, generate a rich and high-quality final response to the user. If there is a clear answer, provide it first, then add a high-quality, natural, and human-like explanatory paragraph. Ensure your final response closely follows the <Question>. Output only your final response, without any additional content."""

# search strategies
search_strategies = [('Backtracking',gen_prompt_rethink_Backtracking),('Exploring New Paths',gen_prompt_rethink_Exploring_New_Path),('Verification',gen_prompt_rethink_Verification),('Correction',gen_prompt_rethink_Correction)]

search_strategies_subagents = [('doublecheck',Sentiment_rethinking_doublecheck),('communication',Sentiment_rethinking_communication)]