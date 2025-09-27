from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    CODE = "code"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        try:
            self.text_type = TextType(text_type)
        except ValueError:
            raise ValueError("given text_type is not a valid choice")
        self.url = url

    def __eq__(node1, node2):
        return node1.text == node2.text and node1.text_type == node2.text_type and node1.url == node2.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"