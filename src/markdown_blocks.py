import re
from enum import Enum
from functools import reduce

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = [block_to_html_node(block) for block in blocks]
    return ParentNode(tag="div", children=html_nodes)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block != ""]
    return blocks

def is_block_quote(block):
    for line in block.splitlines():
        if not line.startswith(">"):
            return False
    return True

def is_unordered_list(block):
    for line in block.splitlines():
        if not (line.startswith("* ") or line.startswith("- ")):
            return False
    return True

def is_ordered_list(block):
    for i, line in enumerate(block.splitlines()):
        if not line.startswith(f"{i+1}. "):
            return False
    return True

def block_to_block_type(block):
    if re.match(r"#{1,6} .", block):
        return BlockType.HEADING
    elif len(block.splitlines()) > 1 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif is_block_quote(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.QUOTE:
        return block_quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return block_ul_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return block_ol_to_html_node(block)
    elif block_type == BlockType.CODE:
        return block_code_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return block_heading_to_html_node(block)
    else:
        return block_paragraph_to_html_node(block)

def block_quote_to_html_node(block):
    # Remove the ">" symbol from each line.
    new_lines = []
    for line in block.splitlines():
        if line == ">":
            new_lines.append("")
        else:
            new_lines.append(line[1:])
    new_block = "\n".join(new_lines)

    text_nodes = text_to_textnodes(new_block)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]

    return ParentNode(tag="blockquote", children=html_nodes)

def block_ul_to_html_node(block):
    # Convert each line to an <li> html node.
    li_html_nodes = []
    for line in block.splitlines():
        new_line = line[2:]
        text_nodes = text_to_textnodes(new_line)
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        li_html_nodes.append(ParentNode(tag="li", children=html_nodes))

    return ParentNode(tag="ul", children=li_html_nodes)

def block_ol_to_html_node(block):
    # Convert each line to an <li> html node.
    li_html_nodes = []
    for line in block.splitlines():
        new_line = line[3:]
        text_nodes = text_to_textnodes(new_line)
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        li_html_nodes.append(ParentNode(tag="li", children=html_nodes))

    return ParentNode(tag="ol", children=li_html_nodes)

def block_code_to_html_node(block):
    # Remove the opening and closing backtick lines.
    new_block = "\n".join(block.splitlines()[1:-1])

    text_nodes = text_to_textnodes(new_block)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    code_html_node = ParentNode(tag="code", children=html_nodes)
    return ParentNode(tag="pre", children=[code_html_node])

def block_heading_to_html_node(block):
    # Find the heading size and remove the # symbols from the block
    heading_chars = re.match(r"(#{1,6}) .", block).group(1)
    heading_size = len(heading_chars)
    new_block = block[(heading_size+1):]

    text_nodes = text_to_textnodes(new_block)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return ParentNode(tag=f"h{heading_size}", children=html_nodes)

def block_paragraph_to_html_node(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return ParentNode(tag=f"p", children=html_nodes)
