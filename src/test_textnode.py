import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_equal(self):
        first, second = [], []

        first.append(TextNode("This is a text node", "bold"))
        second.append(TextNode("This is a text node", "bold"))

        first.append(TextNode("This is a text node", "bold", url="http://example.com"))
        second.append(TextNode("This is a text node", "bold", url="http://example.com"))

        first.append(TextNode("This is a text node", "bold", url=None))
        second.append(TextNode("This is a text node", "bold"))

        for first_val, second_val in zip(first, second):
            self.assertEqual(first_val, second_val)

    def test_not_equal(self):
        first, second = [], []

        first.append(TextNode("This is a text node", "bold"))
        second.append(TextNode("This is a text node", "bold", url="http://example.com"))

        first.append(TextNode("This is a text node", "italic", url="http://example.com"))
        second.append(TextNode("This is a text node", "bold", url="http://example.com"))

        first.append(TextNode("This is a text", "bold"))
        second.append(TextNode("This is a text node", "bold"))

        for first_val, second_val in zip(first, second):
            self.assertNotEqual(first_val, second_val)


if __name__ == "__main__":
    unittest.main()
