#!/usr/bin/env python
"""
clu/if_anthropic.py
"""

import os 
from anthropic import Anthropic 
from dodonasession import DodonaSession


models = {
    "default": "claude-3-5-sonnet-20241022",
    "claude35": "claude-3-5-sonnet-20241022",
    "claude": "claude-3-5-sonnet-latest",
}


class Llm:
    def __init__(self, model: str):
        self.model_name = m if (m := models.get(model)) else  model 
        # Checking if the API key is set properly
        if not(key := os.getenv("ANTHROPIC_API_KEY", None)):
            raise Exception(
                "Please set OPENAI_API_KEY environment variable.\nfor details, run: dodona --help"
            )
        try:
            self.client= Anthropic(api_key=key)
        except Exception as ex:
            print(f"exception when trying to get Anthropic client:\n{ex}")

    def ask_question(self, sess: DodonaSession):
        """ send the question to OpenAI """
        try:
            message = self.client.messages.create(
                max_tokens=1024, 
                model=sess.model, 
                messages=sess.get_messages()
            )
            return message.to_dict()['content'][0]['text']
        except Exception as ex:
            print(f"exception trying to get answer from Claude:\n{ex}")
        return None


## end of file
