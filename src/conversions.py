from textnode import TextNode
from textnode import TextType
from leafnode import LeafNode
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid Enum type.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            text = node.text.split(delimiter)
            if len(text) % 2 == 0:
                raise Exception("Invalid markdown syntax!")
            counter = 1
            for str in text:
                if counter % 2 == 1:
                    temp_node = TextNode(str, TextType.TEXT)
                elif counter % 2 == 0:
                    temp_node = TextNode(str, text_type)
                result.append(temp_node)
                counter += 1
    return result
    
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if node.text_type != TextType.TEXT:
            result.append(node)
        elif len(links) == 0:
            result.append(node)
        else:
            after = node.text
            for link_text, link_url in links:
                before, after = after.split(f"[{link_text}]({link_url})", 1)
                if before:
                    result.append(TextNode(before, TextType.TEXT))
                result.append(TextNode(link_text, TextType.LINK, link_url))
            if after:
                result.append(TextNode(after, TextType.TEXT))

    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_images(node.text)
        if node.text_type != TextType.TEXT:
            result.append(node)
        elif len(links) == 0:
            result.append(node)
        else:
            after = node.text
            for image_alt, image_url in links:
                before, after = after.split(f"![{image_alt}]({image_url})", 1)
                if before:
                    result.append(TextNode(before, TextType.TEXT))
                result.append(TextNode(image_alt, TextType.IMAGE, image_url))
            if after:
                result.append(TextNode(after, TextType.TEXT))
    return result

def text_to_textnodes(text):
    result = split_nodes_image(
        split_nodes_link(
        split_nodes_delimiter(
        split_nodes_delimiter(
        split_nodes_delimiter([TextNode(text, TextType.TEXT)], "`", TextType.CODE),
        "_", TextType.ITALIC),
        "**", TextType.BOLD)
        ))
    return result

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for str in blocks:
        new_string = str.strip()
        if new_string:
            result.append(new_string)
    return result

def block_to_blocktype(block):
    heading = re.findall(r"#{1,6}\s\w", block)
    if block.startswith("#") and len(heading) > 0:
        return BlockType.HEADING
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("1. "):
        lines = block.split("\n")
        line_nr = 1
        ord_list = True
        for line in lines:
            if not line.startswith(f"{line_nr}. "):
                ord_list = False
            line_nr += 1
        if ord_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
