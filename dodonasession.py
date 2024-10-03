""" clu/dodonasession.py 

in an attempt to clean up dodona.py, 
the DodonaSession class encapsulates an ongoing Q&A with dodona 
"""

from domible.elements import Html, Body, Title, BaseElement
from domible.elements import Heading, Anchor, Paragraph, HorizontalRule, Div
from domible.elements import UnorderedList, ListItem
from domible.starterDocuments import basic_head_empty_body
from domible.tools import open_html_in_browser


class DodonaSession:
    @staticmethod
    def create_system_message(txt: str):
        return {"role": "system", "content": txt}
    @staticmethod
    def create_user_message(txt: str):
        return {"role": "user", "content": txt}
    @staticmethod
    def create_assistant_message(txt: str):
        return {"role": "assistant", "content": txt}

    def __init__(self, model: str, system: str = None, question: str = None):
        self.model: str = model 
        self.messages = list()
        if system: self.messages.append(self.create_system_message(system))
        if question: self.messages.append(self.create_user_message(question))

    def add_system_message(self, txt: str):
        self.messages.append(self.create_system_message(txt))

    def add_user_message(self, txt: str):
        self.messages.append(self.create_user_message(txt))

    def add_assistant_message(self, txt: str):
        self.messages.append(self.create_assistant_message(txt))

    def get_messages(self):
        return self.messages 

    @staticmethod
    def get_html_from_message(msg: dict[str, str]) -> BaseElement:
        match msg['role']:
            case 'system':
                return Div([Heading(2, "System"), Paragraph(msg['content'])], **{'class': 'system'})
            case 'user':
                return Div([Heading(2, "User"), Paragraph(msg['content'])], **{'class': 'user'})
            case 'assistant':
                return Div([Heading(2, "Assistant"), Paragraph(msg['content'])], **{'class': 'assistant'})
            case _:
                return Div([Heading(2, "Unknown Role"), Paragraph(msg['content'])], **{'class': 'unknown-role'})

    def open_in_browser(self, title: str = "Dodona Session"):
        """ show this session in default browser """
        html_doc: Html = basic_head_empty_body(title)
        body = html_doc.get_body_element()
        body.add_content([
            Heading(1, title),
            UnorderedList([ListItem(self.model)])
        ])
        for msg in self.messages:
            # create HTML for the msg and add it to the body 
            body.add_content(self.get_html_from_message(msg))
        open_html_in_browser(html_doc)


## end of file
