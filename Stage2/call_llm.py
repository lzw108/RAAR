import json

from openai import OpenAI
from retrying import retry


class DeepSeek:
    def __init__(self, version):
        api_key = ""
        base_url = "https://api.deepseek.com"


        self.version = version
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def call(self, content, additional_args=None):
        messages = [{'role': 'user', 'content': content}]
        if additional_args is None:
            additional_args = {}


        completion = self.client.chat.completions.create(
            model=self.version,
            messages=messages,
            max_completion_tokens=8192,
            temperature=1
        )
        answer = completion.choices[0].message.content
        if answer.strip() == "broken":
            self.call(messages)
        return answer

    @retry(wait_fixed=3000, stop_max_attempt_number=3)
    # def retry_call(self, content, additional_args={"max_tokens": 8192}):
    def retry_call(self, content, additional_args=None):
        if additional_args is None:
            additional_args = {"max_completion_tokens": 8190}
        return self.call(content, additional_args)