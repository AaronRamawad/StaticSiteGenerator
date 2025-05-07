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
        if len(split_segments) == 1:
            new_nodes.append(old_node)
        elif len(split_segments) % 2 == 0:
            raise ValueError("Invalid Markdown, format is not closed")
        else:
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
        link_text, link = markdown.split("(")

        link_text = link_text.lstrip("[").rstrip("]")
        link = link.rstrip(")")

        links.append((link_text, link))

    return links

def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        else:
            sections = node.text.split(f"[{links[0][0]}]({links[0][1]})")
            if len(links) > 1:
                for i in range(1, len(links)):
                    new_sections = sections.pop(i).split(f"[{links[i][0]}]({links[i][1]})")
                    for section in new_sections:
                        sections.append(section)

            for i in range(len(sections)):
                if sections[i] == "" or sections[i] == " ":
                    sections.pop(i)
                else:
                    new_nodes.append(TextNode(sections[i], TextType.TEXT))
                try:
                    new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                except IndexError:
                    pass
        
    return new_nodes


def split_nodes_image(old_nodes):
    
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        else:
            sections = node.text.split(f"![{images[0][0]}]({images[0][1]})")
            if len(images) > 1:
                for i in range(1, len(images)):
                    new_sections = sections.pop(i).split(f"![{images[i][0]}]({images[i][1]})")
                    for section in new_sections:
                        sections.append(section)

            for i in range(len(sections)):
                if sections[i] == "" or sections[i] == " ":
                            sections.pop(i)
                else:
                    new_nodes.append(TextNode(sections[i], TextType.TEXT))
                try:
                    new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                except IndexError:
                    pass

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_image([node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip("\n").strip()
        if blocks[i] == "" or blocks[i] == "\n":
            blocks.pop[i]
    return blocks
