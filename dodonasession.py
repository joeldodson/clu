""" clu/dodonasession.py 

in an attempt to clean up dodona.py, 
the DodonaSession class encapsulates an ongoing Q&A with dodona 

I created this after only using the OpenAI API.
While trying to integrate the Google GenAI  API, 
I realized how specific this is to how Chat GPT works.
I've squeezed part of the Google GenAI API into this format,
and it works well in the command line in the question and answer format.
I'm thinking long term though, it would be better to have a didferent app for each provider.
Or at least some redesign/restructuring is in order.

Until then, which might be never, there's going to be some hackery.
"""

from domible.elements import Html, Body, Title, BaseElement
from domible.elements import Heading, Anchor, Paragraph, HorizontalRule, Div
from domible.elements import UnorderedList, ListItem
from domible.starterDocuments import basic_head_empty_body
from domible.tools import open_html_in_browser


class DodonaSession:
    """
    adding some items in the session that might be accessed from 
    each provider as well as from dodona itself.
    """
##     answer_output_specification = "Please respond to all questions in html.  Do not respond with complete docs, that is, do not use html, head, and body elements.  Use semantic elements appropriate for specific content.  For example, use paragraph, lists, anchors, and headings elements where appropriate. "
    answer_output_specification = "please respond to all questions using standard github markdown"
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
        ## if system: self.messages.append(self.create_system_message(system))
        if question: self.messages.append(self.create_user_message(question))

    def add_system_message(self, txt: str):
        ## self.messages.append(self.create_system_message(txt))
        pass 

    def add_user_message(self, txt: str):
        self.messages.append(self.create_user_message(txt))

    def add_assistant_message(self, txt: str):
        self.messages.append(self.create_assistant_message(txt))

    def get_messages(self):
        return self.messages 

    def get_last_message(self):
        return self.messages[len(self.messages) - 1]["content"]

    @staticmethod
    def get_html_from_message(msg: dict[str, str]) -> BaseElement:
        match msg['role']:
            case "system":
                return Div(
                    [Heading(2, "System"), Paragraph(msg["content"])],
                    **{"class": "system"},
                )
            case 'user':
                return Heading(2, msg['content'], **{'class': 'user'})
            case 'assistant':
                return Div([Heading(2, "Answer"), Paragraph(msg['content'])], **{'class': 'assistant'})
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
