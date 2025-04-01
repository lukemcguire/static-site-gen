import unittest
from enum import Enum, auto

from main import markdown_to_html_node, text_node_to_html_node
from textnode import TextNode, TextType


class TestMain(unittest.TestCase):
    def test_text_node_to_html_node_normal(self):
        text_node = TextNode("Normal text", TextType.TEXT)
        leaf_node = text_node_to_html_node(text_node)
        self.assertIsNone(leaf_node.tag)
        self.assertEqual(leaf_node.value, "Normal text")
        self.assertIsNone(leaf_node.props)
        self.assertIsNone(leaf_node.children)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "Bold text")
        self.assertIsNone(leaf_node.props)
        self.assertIsNone(leaf_node.children)

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "Italic text")
        self.assertIsNone(leaf_node.props)
        self.assertIsNone(leaf_node.children)

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "Code text")
        self.assertIsNone(leaf_node.props)
        self.assertIsNone(leaf_node.children)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Link text", TextType.LINK, "https://example.com")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "Link text")
        self.assertEqual(leaf_node.props, {"href": "https://example.com"})
        self.assertIsNone(leaf_node.children)

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Image alt text", TextType.IMAGE, "https://example.com/image.png")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(leaf_node.props, {"src": "https://example.com/image.png", "alt": "Image alt text"})
        self.assertIsNone(leaf_node.children)

    def test_text_node_to_html_node_unknown(self):
        class UnknownTextType(Enum):
            UNKNOWN = auto()

        text_node = TextNode("Unknown text", UnknownTextType.UNKNOWN)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Unknown text type.")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

# Not yet implemented due to how we're currently parsing blocks
#     def test_multiple_headings(self):
#         md = """
# # Heading 1
# ## Heading 2
# ### Heading 3
# """
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(html, "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>")

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_ordered_list(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>")

    def test_quote(self):
        md = """> This is a quote
> with multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote with multiple lines</blockquote></div>")


if __name__ == "__main__":
    unittest.main()
