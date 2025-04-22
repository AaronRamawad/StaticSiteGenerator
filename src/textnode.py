from enum import Enum
from htmlnode import HTMLNode, LeafNode
from regex import findall

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
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if type == TextType.IMAGE:
        return LeafNode("img", "", {
            "src": text_node.url,
            "alt": text_node.text,
        })
    
# It could look like this "This is a **text block** where **text** stays"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        split_segments = old_node.text.split(delimiter)
        if len(split_segments) % 2 == 0:
            raise ValueError("Invalid Markdown, format is not closed")
        for i in range(len(split_segments)):
            if split_segments[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_segments[i], old_node.text_type))
            else:
                new_nodes.append(TextNode(split_segments[i], text_type))
                
    return new_nodes


def extract_markdown_images(text):

    images = []

    #looks for ![rick roll](https://i.imgur.com/aKaOqIh.gif)
    image_markdowns = findall(r"!\[.*?\]\(.*?\)", text)

    for markdown in image_markdowns:
        alt, link = markdown.split("(")

        alt = alt.lstrip("![").rstrip("]")
        link = link.rstrip(")")

        images.append((alt, link))

    return images

def extract_markdown_links(text):

    links = []

    #looks for [to youtube](https://www.youtube.com/@bootdotdev)
    link_markdowns = findall(r"\[.*?\]\(.*?\)", text)

    for markdown in link_markdowns:
        alt, link = markdown.split("(")

        alt = alt.lstrip("[").rstrip("]")
        link = link.rstrip(")")

        links.append((alt, link))

    return links