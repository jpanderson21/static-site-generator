import re

from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_text = node.text.split(delimiter)
            num_splits = len(split_text)
            if num_splits % 2 == 0:
                raise Exception("Invalid Markdown syntax.")
            inner_nodes = []
            for index, item in enumerate(split_text):
                if len(item) > 0:
                    if index % 2 == 0:
                        inner_nodes.append(TextNode(item, TextType.TEXT))
                    else:
                        inner_nodes.append(TextNode(item, text_type))
            new_nodes.extend(inner_nodes)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            inner_nodes = []
            text = node.text
            images = extract_markdown_images(text)
            for image in images:
                image_tag = f"![{image[0]}]({image[1]})"
                split_text = text.split(image_tag, 1)
                if len(split_text[0]) > 0:
                    inner_nodes.append(TextNode(split_text[0], TextType.TEXT))
                inner_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                text = split_text[1]
            if len(text) > 0:
                inner_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.extend(inner_nodes)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            inner_nodes = []
            text = node.text
            links = extract_markdown_links(text)
            for link in links:
                link_tag = f"[{link[0]}]({link[1]})"
                split_text = text.split(link_tag, 1)
                if len(split_text[0]) > 0:
                    inner_nodes.append(TextNode(split_text[0], TextType.TEXT))
                inner_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                text = split_text[1]
            if len(text) > 0:
                inner_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.extend(inner_nodes)
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
