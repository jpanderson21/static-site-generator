import unittest

from markdown_blocks import *

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        expectations, results = [], []

        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        results.append(markdown_to_blocks(text))
        expectations.append([
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ])

        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        results.append(markdown_to_blocks(text))
        expectations.append([
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ])

        text = """

This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line


* This is a list
* with items

"""
        results.append(markdown_to_blocks(text))
        expectations.append([
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ])

        text = "This is **bolded** paragraph"
        results.append(markdown_to_blocks(text))
        expectations.append([
            "This is **bolded** paragraph",
        ])

        text = ""
        results.append(markdown_to_blocks(text))
        expectations.append([])

        text = "  \n\n"
        results.append(markdown_to_blocks(text))
        expectations.append([])

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_block_to_block_type(self):
        expectations, results = [], []

        text = "# heading"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.HEADING)

        text = "#heading"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = "###### heading"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.HEADING)

        text = "####### heading"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = "!# heading"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = "```not code```"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = "``code\n```"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = "```code\n``"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = """```
        some
        code
        ```"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.CODE)

        text = "```code\n```"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.CODE)

        text = """>this
>is
>a
>quote"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.QUOTE)

        text = """>this
>is
not
>a
>quote"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = """>this
>is
>not
>a

>quote"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = ">quote"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.QUOTE)

        text = "* list"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.UNORDERED_LIST)

        text = "*not-a-list"
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = """* this
* is
* a
- list"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.UNORDERED_LIST)

        text = """* this
* is
not
* a
- list"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = """1. an
2. ordered
3. list"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.ORDERED_LIST)

        text = """1. an
2. ordered
3. list
(not)"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = """1.not
2. an
3. ordered
4. list"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        text = """1. not
2. an
3. ordered
3. list"""
        results.append(block_to_block_type(text))
        expectations.append(BlockType.PARAGRAPH)

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_block_quote_to_html(self):
        expectations, results = [], []

        block = """>This
>is
>a
>quote"""
        expectations.append("""<blockquote>This
is
a
quote</blockquote>""")
        results.append(block_to_html_node(block).to_html())

        block = """>This
>**is**
>a
>quote"""
        expectations.append("""<blockquote>This
<b>is</b>
a
quote</blockquote>""")
        results.append(block_to_html_node(block).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_block_ul_to_html(self):
        expectations, results = [], []

        block = """* This
* is
* a
* list"""
        expectations.append("""<ul><li>This</li><li>is</li><li>a</li><li>list</li></ul>""")
        results.append(block_to_html_node(block).to_html())

        block = """* This
* **is**
* a
* list"""
        expectations.append("""<ul><li>This</li><li><b>is</b></li><li>a</li><li>list</li></ul>""")
        results.append(block_to_html_node(block).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_block_ol_to_html(self):
        expectations, results = [], []

        block = """1. This
2. is
3. a
4. list"""
        expectations.append("""<ol><li>This</li><li>is</li><li>a</li><li>list</li></ol>""")
        results.append(block_to_html_node(block).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_block_code_to_html(self):
        expectations, results = [], []

        block = """```
int i = 0
i++
```"""
        expectations.append("""<pre><code>int i = 0\ni++</code></pre>""")
        results.append(block_to_html_node(block).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_block_heading_to_html(self):
        expectations, results = [], []

        block = """### H3 Heading"""
        expectations.append("""<h3>H3 Heading</h3>""")
        results.append(block_to_html_node(block).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_block_paragraph_to_html(self):
        expectations, results = [], []

        block = """This is a paragraph."""
        expectations.append("""<p>This is a paragraph.</p>""")
        results.append(block_to_html_node(block).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)

    def test_markdown_to_html(self):
        expectations, results = [], []

        markdown = """### H3 Heading

```
# some code
int i = 0
```

[example link](http://example.com)

Some plain text."""
        expectations.append("""<div><h3>H3 Heading</h3><pre><code># some code\nint i = 0</code></pre><p><a href=\"http://example.com\">example link</a></p><p>Some plain text.</p></div>""")
        results.append(markdown_to_html_node(markdown).to_html())

        for expected, result in zip(expectations, results):
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
