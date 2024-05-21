import unittest

from textnode import *
from inline_markdown import *


class TestInlineMarkdown(unittest.TestCase):
    def test_text_to_html(self):
        expectations, results = [], []

        expectations.append('some text')
        text_node = TextNode(text="some text", text_type=TextType.TEXT)
        results.append(text_node_to_html_node(text_node).to_html())

        expectations.append('<b>some bold text</b>')
        text_node = TextNode(text="some bold text", text_type=TextType.BOLD)
        results.append(text_node_to_html_node(text_node).to_html())

        expectations.append('<i>some italic text</i>')
        text_node = TextNode(text="some italic text", text_type=TextType.ITALIC)
        results.append(text_node_to_html_node(text_node).to_html())

        expectations.append('<code>hello world</code>')
        text_node = TextNode(text="hello world", text_type=TextType.CODE)
        results.append(text_node_to_html_node(text_node).to_html())

        expectations.append('<a href="http://example.com">my link</a>')
        text_node = TextNode(text="my link", text_type=TextType.LINK, url="http://example.com")
        results.append(text_node_to_html_node(text_node).to_html())

        expectations.append('<img src="http://example.com/circle.jpg" alt="circle"></img>')
        text_node = TextNode(text="circle", text_type=TextType.IMAGE, url="http://example.com/circle.jpg")
        results.append(text_node_to_html_node(text_node).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)


    def test_split_nodes(self):
        expectations, results = [], []

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        results.append(split_nodes_delimiter([node], "`", TextType.CODE))
        expectations.append([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

        node = TextNode("This is text with a `code block` and **bold** text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        results.append(split_nodes_delimiter(new_nodes, "**", TextType.BOLD))
        expectations.append([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ])

        node = TextNode("`only a code block`", TextType.TEXT)
        results.append(split_nodes_delimiter([node], "`", TextType.CODE))
        expectations.append([
            TextNode("only a code block", TextType.CODE),
        ])

        node = TextNode("*starting* with italic", TextType.TEXT)
        results.append(split_nodes_delimiter([node], "*", TextType.ITALIC))
        expectations.append([
            TextNode("starting", TextType.ITALIC),
            TextNode(" with italic", TextType.TEXT),
        ])

        node = TextNode("ending with **bold**", TextType.TEXT)
        results.append(split_nodes_delimiter([node], "**", TextType.BOLD))
        expectations.append([
            TextNode("ending with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)


    def test_image_extraction(self):
        expectations, results = [], []

        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        results.append(extract_markdown_images(text))
        expectations.append([("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

        text = "This is text without an image"
        results.append(extract_markdown_images(text))
        expectations.append([])

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_link_extraction(self):
        expectations, results = [], []

        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        results.append(extract_markdown_links(text))
        expectations.append([("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

        text = "This is text without a link"
        results.append(extract_markdown_links(text))
        expectations.append([])

        text = "This is text without a link but with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        results.append(extract_markdown_links(text))
        expectations.append([])

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_split_nodes_image(self):
        expectations, results = [], []

        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ])

        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) ",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
            TextNode(" ", TextType.TEXT),
        ])

        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) ",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
            TextNode(" ", TextType.TEXT),
        ])

        node = TextNode(
            " ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" ", TextType.TEXT),
        ])

        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" ", TextType.TEXT),
        ])

        node = TextNode(
            " ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ])

        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ])

        node = TextNode(
            "This is text without an image.",
            TextType.TEXT,
        )
        results.append(split_nodes_image([node]))
        expectations.append([
            TextNode("This is text without an image.", TextType.TEXT),
        ])

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_split_nodes_link(self):
        expectations, results = [], []

        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT,
        )
        results.append(split_nodes_link([node]))
        expectations.append([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ])

        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT,
        )
        results.append(split_nodes_link([node]))
        expectations.append([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", TextType.TEXT),
        ])

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_text_to_nodes(self):
        expectations, results = [], []

        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        results.append(text_to_textnodes(text))
        expectations.append([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

        text = "This is text."
        results.append(text_to_textnodes(text))
        expectations.append([
            TextNode("This is text.", TextType.TEXT),
        ])

        text = "This is **bold text** with more **bold text** and two `code` `blocks` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)."
        results.append(text_to_textnodes(text))
        expectations.append([
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with more ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and two ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("blocks", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(".", TextType.TEXT),
        ])

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
