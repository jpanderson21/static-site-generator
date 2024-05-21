import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        expectations, results = [], []

        expectations.append(' href="https://www.google.com" target="_blank"')
        results.append(HTMLNode(props={"href": "https://www.google.com", "target": "_blank"}).props_to_html())

        expectations.append(' src="https://www.example.com/img.png"')
        results.append(HTMLNode(props={"src": "https://www.example.com/img.png"}).props_to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        expectations, results = [], []

        results.append(LeafNode("p", "This is a paragraph of text.").to_html())
        expectations.append('<p>This is a paragraph of text.</p>')

        results.append(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html())
        expectations.append('<a href="https://www.google.com">Click me!</a>')

        results.append(LeafNode("a", "Click me!", {"href": "https://www.google.com", "class": "my-link"}).to_html())
        expectations.append('<a href="https://www.google.com" class="my-link">Click me!</a>')

        results.append(LeafNode(None, "raw text").to_html())
        expectations.append('raw text')

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        expectations, results = [], []

        expectations.append('<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
        results.append(ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ).to_html())

        expectations.append('<p class="my-paragraph"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
        results.append(ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "my-paragraph"}
        ).to_html())

        expectations.append('<div class="my-div" style="background-color: white">Normal text<i>italic text</i><p><h1>header text</h1><h2>more header text</h2></p></div>')
        results.append(ParentNode(
            "div",
            [
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode("p", [LeafNode("h1", "header text"), LeafNode("h2", "more header text")]),
            ],
            {"class": "my-div", "style": "background-color: white"}
        ).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
