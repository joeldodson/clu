#!/usr/bin/env python
""" clu/dodona.py 
This was initially a very simple script to ask a single question to ChatGPT.
I then wanted to extend it to ask follow up questions.
And with that, thought it'd be nice to view the history in a browser.
It has become a bit unruly and maybe should be split into modules. 
I did split out management of a single session (series of questions and answers)
into a separate module: dodonasession.py 
"""

import sys 
import os
from pathlib import Path 

from openai import OpenAI
import markdown 

from dodonasession import DodonaSession 

chat_models = {
    "default": "gpt-4o-mini",
    "35t": "gpt-3.5-turbo",
    "4o": "gpt-4o",
    "4omini": "gpt-4o-mini",
}

## Define the command line interface
import argparse
dodona_description = """Access the OpenAI Chat API to ask questions.
You need an OpenAI account and API key, see: 
https://platform.openai.com/docs/introduction 
The API key is expected in an environment variable: 
OPENAI_API_KEY 
You'll also need the openai python package, run: 
pip install --upgrade openai 
Any options without defaults and not entered via command line will be queried by dodona.
be sure to surround command line string arguments with double quotes.
after processing your first question,
dodona will provide a prompt, "dodona", at which point you can:  
type "quit" to exit dodona 
type "oib" to have the current session Opened In Browser,
type a follo-on question to continue the session 
"""

model_help = """which Chat GPT model to use for this session.  Options are:
35t: the gpt-3.5-turbo,
4omini (default): gpt-4o-mini,
4o: gpt-4o,
your own string: This is so you can try any valid string you find on the OpenAI website.  
"""

system_help = """describe the type of system you want answering your question.  For example:
"an expert python developer with extensive experience with flask, jinja, and html"
"""

question_help = """your curiosity is the limit.
"""
file_help = """ use instead of a question to support  larger inputs.
The file will be opened and used as the "content" for the initial question 
"""

parser = argparse.ArgumentParser(prog="dodona",
                                 description=dodona_description ,
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog="Cheers!")
parser.add_argument("-m", "--model", default="default", help=model_help)
parser.add_argument("-q", "--question", help=question_help)
parser.add_argument("-s", "--system", help=system_help)
parser.add_argument("-f", "--file", help=file_help)
args = parser.parse_args()


_client = None
def get_openai_client():
    global _client
    if _client is None:
        # Checking if the API key is set properly
        if not os.getenv("OPENAI_API_KEY", None):
            raise Exception("Please set OPENAI_API_KEY environment variable.\nfor details, run: dodona --help")
        try:
            _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as ex:
            print(f"exception when trying to get OpenAI  client:\n{ex}") 
            _client = None 
    return _client


def get_system():
    """
    ask the user to describe the characteristics of the system being queried.
    E.g., "you are an expert python developer with deep knowledge of flask, django, and fastapi"  
    Or, "you are a historian specializing in ancient Egypt"
    """
    system = ""
    while len(system) == 0:
        system = input("Tell Dodona domain knowledge needed to answer these questions: ")
    return system


def get_question():
    """
    ask the user for the question to ask
    """
    question = ""
    while len(question) == 0:
        question = input("Dodona: ").strip()
    return question 


def ask_question(sess: DodonaSession):
    """ send the question to OpenAI """
    completion = None
    try:
        completion = get_openai_client().chat.completions.create(
            model=sess.model,
            messages=sess.get_messages()
        )
    except Exception as ex:
        print(f"exception trying to get completion:\n{ex}")

    return completion


if __name__ == "__main__":
    model = m if (m := chat_models.get(args.model)) else args.model
    system = args.system if args.system else get_system()
    print(f"questions will be answered useing model: \n {model} n with system background as: \n {system}")
    sess: DodonaSession = DodonaSession(model, system)

    if args.file:
        question = Path(args.file).read_text(encoding = 'utf-8')
    else:
        question = args.question if args.question else get_question()
    while True:
        if question.lower() == "quit": break
        if question.lower() == 'oib': sess.open_in_browser()
        else:
            sess.add_user_message(question)
            answer = ask_question(sess)
            if answer:
                answer_md = answer.choices[0].message.content
                print(answer_md)
                sess.add_assistant_message(markdown.markdown(answer_md))
            else:
                print("could not get an answer for you")
                sess.add_assistant_message("Some questions do not have answers.")
        question = get_question()
    print("Mazel Tov!")

## end of file
