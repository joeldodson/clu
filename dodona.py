#!/usr/bin/env python
""" clu/dodona.py 
This was initially a very simple script to ask a single question to ChatGPT.
I then wanted to extend it to ask follow up questions.
And with that, thought it'd be nice to view the history in a browser.
And from there, thought it'd be nice to invite Claude (Anthropic) to the party
and, of course, Google Gemini 

This has become a hack job.
The Python SDKs from OpenAI, Anthropic, and Google
are simlar enough to allow basic threads of Q&A.
They are different enough though my original, hastily contrived approach is wearing thin.
I'll check this in and maybe rewrite it someday.
"""

import importlib 
import sys 
import os
from pathlib import Path 

import markdown 
from dodonasession import DodonaSession 

"""
to support multiple APIs, 
llm_providers is a mapping from a string the user gives to specifiy which model,
to a string of the module implementing that interface 
"""
llm_providers = {
    "default": "if_openai",
    "4o": "if_openai",
    "4omini": "if_openai",
    "gf20": "if_google",
    "gf15": "if_google",
    "claude": "if_anthropic",
    "claude35": "if_anthropic",
}

## Define the command line interface
import argparse
dodona_description = """Access your favorite LLM to ask questions.
currently supporting OpenAI, Anthropic, and Google (see below for requirements for each) 

Any options without defaults and not entered via command line will be queried by dodona.
be sure to surround command line string arguments with double quotes.
after processing your first question,
dodona will provide a prompt, "dodona", at which point you can:  
type "quit" to exit dodona 
type "oib" to have the current session Opened In Browser,
type "wtf <filename>" to write the current session to a file.  ALERT: FILE WILL BE TRUNCATED
type "model" to have the model name printed 
type a follo-on question to continue the session 

for OpenAI: You need an OpenAI account and API key, see: 
https://platform.openai.com/docs/introduction 
The API key is expected in an environment variable: 
OPENAI_API_KEY 
You'll also need the openai python package, run: 
pip install --upgrade openai 

for Anthropic:
you need an API key in environment variable:
ANTHROPIC_API_KEY

And you need the anthropic Python package:

pip install anthropic 

to get started, and get an API key, see:

https://docs.anthropic.com/en/api/getting-started

for Google: You need a google account and API key, see: 
https://platform.openai.com/docs/introduction 
The API key is expected in an environment variable: 
GEMINI_API_KEY 
You'll also need the google-genai python package, run: 
pip install --upgrade google-genai
"""

model_help = """which model to use for this session.  Options are:
4o: gpt-4o (default),
4omini: gpt-4o-mini,
your own string: This is so you can try any valid string you find on the OpenAI website.  
If you specify your own string, you must also specify the name of the module to import
for example, though it's not listed, The same OpenAI API supports the o1 model.
I could enter "-m o1 -p openai" 
"""

provider_help = """ the name of the module implementing the API for the chosen model.
this is only needed if the specified model is not listed as an option in -m 
"""

system_help = """describe the type of system you want answering your question.  For example:
"an expert python developer with extensive experience with flask, jinja, and html"
"""

question_help = """your curiosity is the limit.
"""
infile_help = """ use instead of a question to support  larger inputs.
The file will be opened and used as the "content" for the initial question 
For example, I might take a .css file and add to the top of it:
'explain the following css as though I have very little web development experience',
then specify that as the infile.
"""

parser = argparse.ArgumentParser(prog="dodona",
                                 description=dodona_description ,
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog="Cheers!")
parser.add_argument("-m", "--model", default="default", help=model_help)
parser.add_argument("-p", "--provider", help=provider_help)
parser.add_argument("-q", "--question", help=question_help)
parser.add_argument("-s", "--system", help=system_help)
parser.add_argument("-i", "--infile", help=infile_help)
args = parser.parse_args()


def get_system():
    """
    ask the user to describe the characteristics of the system being queried.
    E.g., "you are an expert python developer with deep knowledge of flask, django, and fastapi"  
    Or, "you are a historian specializing in ancient Egypt"

    Turns out Google Gemini does not use a "system" role.
    It derives it as the chat progresses.
    Allow system to be empty.
    """
    system = ""
    while len(system) == 0:
        system = input("Tell Dodona domain knowledge needed to answer these questions (type 'none' for no system): ")
        if system.lower() == 'none':
            system = None
            break 
    return system


def get_question():
    """
    ask the user for the question to ask
    """
    question = ""
    while len(question) == 0:
        question = input("Dodona: ").strip()
    return question 


def write_output(output: str, outfile: str, append: bool):
    if not append:
        Path(outfile).write_text(output, encoding='utf-8')
    else:
        with Path(outfile).open('a', encoding='utf-8') as f:
            f.write(output)


def get_llm():
    if not (provider := llm_providers.get(args.model)):
        if not (provider := args.provider):
            print(f"the modle {args.model} is not known, you must also specify the provider.")
            return None
    try:
        module = importlib.import_module(provider)
        print(f"successfully imported module {provider}")
        return module.Llm(args.model)
    except ImportError as ex:
        print(f"failed to import module {provider}, with exception \n{ex}")
    return None 


if __name__ == "__main__":
    if not (llm := get_llm()):    
        print(f"failed to get llm for model {args.model}")
        exit(1)
    system = args.system if args.system else get_system()
    if system: system += DodonaSession.answer_output_specification 
    print(f"questions will be answered useing model: \n {llm.model_name} n with system background as: \n {system}")
    sess: DodonaSession = DodonaSession(llm.model_name, system)

    if args.infile:
        question = Path(args.infile).read_text(encoding = 'utf-8')
    else:
        question = args.question if args.question else get_question()
    while True:
        if question.lower() in ["quit", "exit"]: break
        if question.lower() == 'oib': 
            sess.open_in_browser()
        elif question.lower() == "model":
            print(f"using model: {sess.model}")
        elif question.split()[0].lower() == 'wtf':
            print(f"Write To File: {question.split()[1]} NOT YET IMPLEMENTED")
        else:
            sess.add_user_message(question)
            answer = llm.ask_question(sess)
            if answer:
                print(answer)
                ## sess.add_assistant_message(answer)
                sess.add_assistant_message(markdown.markdown(answer))
            else:
                print("could not get an answer for you")
                sess.add_assistant_message("Some questions do not have answers.")
        question = get_question()
    print("Mazel Tov!")

## end of file
