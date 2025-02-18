#!/usr/bin/env python
"""
clu/if_google.py
"""

import os 
from google import genai
from google.genai import types
from dodonasession import DodonaSession


models = {
    "default": "gemini-2.0-flash",
    "gf20": "gemini-2.0-flash",
    "gf15": "gemini-1.5-flash",
}


class Llm:
    def __init__(self, model: str):
        self.model_name = m if (m := models.get(model)) else  model 
        # Checking if the API key is set properly
        if not(key := os.getenv("GEMINI_API_KEY", None)):
            raise Exception(
                "Please set GEMINI_API_KEY environment variable.\nfor details, run: dodona --help"
            )
        try:
            self.client= genai.Client(api_key=key)   
            self.chat = self.client.chats.create(model=self.model_name)
        except Exception as ex:
            print(f"exception when trying to get Google Genai client:\n{ex}")

    def ask_question(self, sess: DodonaSession):
        """ 
        send the question to google genai 
        It's a little hacky in here since dodona was initially written for only Chat GPT and the OpenAI API.
        There are some differences I'm trying to keep contained in this module.
        Google Genai doesn't use a 'system' role for example.
        """
        try:
            question = sess.get_last_message()
            if len(sess.messages) == 1:
                # this is the first message in the chat,
                # it's like the 'system' message in OpenAI.
                # append text telling Genai to use html
                question += sess.answer_output_specification
            response = self.chat.send_message(question)
            return response.text 
        except Exception as ex:
            print(f"exception trying to get genai response:\n{ex}")
        return None


## end of file
