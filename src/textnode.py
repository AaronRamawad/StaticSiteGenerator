from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textNode):
        return (self.text == textNode.text 
                and self.text_type == textNode.text_type 
                and self.url == textNode.url)
    
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type.value}, {self.url})")
    
def text_node_to_html_node(text_node):
    type = text_node.text_type

    if not type in list(TextType):
        raise Exception("Not in Text Type")
    
    if type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if type == TextType.LINK:
        return LeafNode("a", text_node.value, {"href": text_node.url})
    if type == TextType.IMAGE:
        return LeafNode("img", "", {
            "src": text_node.url,
            "alt": text_node.text,
        })
    


    