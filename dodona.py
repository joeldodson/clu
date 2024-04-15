#!/usr/bin/env python
""" clu/dodona.py """

import sys 
import os
from openai import OpenAI

chat_models = {
    "default": "gpt-3.5-turbo",
    "35t": "gpt-3.5-turbo",
    "40": "gpt-4.0",
    "40t": "gpt-4.0-turbo"
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
"""

model_help = """which Chat GPT model to use for this session.  Options are:
35t (default): the gpt-3.5-turbo,
40: gtp-4.0,
40t: gpt-4.0-turbo,
your own string: This is so you can try any valid string you find on the OpenAI website.  
"""

system_help = """describe the type of system you want answering your question.  For example:
"an expert python developer with extensive experience with flask, jinja, and html"
"""

question_help = """your curiosity is the limit.
"""

parser = argparse.ArgumentParser(prog="dodona",
                                 description=dodona_description ,
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog="Cheers!")
parser.add_argument("-m", "--model", default="default", help=model_help)
parser.add_argument("-q", "--question", help=question_help)
parser.add_argument("-s", "--system", help=system_help)
args = parser.parse_args()


_client = None

def get_openai_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    return _client


# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")
else:
    get_openai_client()


def ask_question(model: str, system: str, question: str): 
    """
    """
    completion = _client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                ## "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
                "content": system,
            },
            {
                "role": "user",
                ## "content": "Compose a poem that explains the concept of recursion in programming.",
                "content": question,
            },
        ],
    )
    return completion 


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
        question = input("Ask Dodona your question: ")
    return question 


if __name__ == "__main__":
    model = m if (m := chat_models.get(args.model)) else args.model
    system = args.system if args.system else get_system()
    print(f"questions will be answered useing model: \n {model} n with system background as: \n {system}")
    
    question = args.question if args.question else get_question()
    while True:
        if question == "quit": break
        answer = ask_question(model, system, question)
        print(answer.choices[0].message.content)
        question = get_question().strip()

    print("Mazel Tov!")

## end of file
