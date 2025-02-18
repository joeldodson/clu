#!/usr/bin/env python
"""
clu/if_openai.py
"""

import os 
from openai import OpenAI
from dodonasession import DodonaSession


models = {
    "default": "gpt-4o",
    "4o": "gpt-4o",
    "4omini": "gpt-4o-mini",
}


class Llm:
    def __init__(self, model: str):
        self.model_name = m if (m := models.get(model)) else  model 
        # Checking if the API key is set properly
        if not(key := os.getenv("OPENAI_API_KEY", None)):
            raise Exception(
                "Please set OPENAI_API_KEY environment variable.\nfor details, run: dodona --help"
            )
        try:
            self.client= OpenAI(api_key=key)
        except Exception as ex:
            print(f"exception when trying to get OpenAI  client:\n{ex}")

    def ask_question(self, sess: DodonaSession):
        """ send the question to OpenAI """
        try:
            completion = self.client.chat.completions.create(
                model=sess.model,
                messages=sess.get_messages()
            )
            return completion.choices[0].message.content
        except Exception as ex:
            print(f"exception trying to get completion:\n{ex}")
        return None


## end of file
