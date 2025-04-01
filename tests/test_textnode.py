import unittest
from enum import Enum, auto

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq_one_url_none(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_both_url_none(self):
        node = TextNode("This is a link", TextType.LINK)
        node2 = TextNode("This is a link", TextType.LINK)
        self.assertEqual(node, node2)

    def test_eq_different_object(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a string")

    def test_repr(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a link, LINK, https://www.boot.dev)")

    def test_repr_no_url(self):
        node = TextNode("This is bold text", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is bold text, BOLD, None)")

    def test_init_normal(self):
        node = TextNode("Normal text", TextType.TEXT)
        self.assertEqual(node.text, "Normal text")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_init_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        self.assertEqual(node.text, "Bold text")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertIsNone(node.url)

    def test_init_link(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Link text")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    def test_init_image(self):
        node = TextNode("Image text", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(node.text, "Image text")
        self.assertEqual(node.text_type, TextType.IMAGE)
        self.assertEqual(node.url, "https://example.com/image.png")

    def test_init_code(self):
        node = TextNode("Code text", TextType.CODE)
        self.assertEqual(node.text, "Code text")
        self.assertEqual(node.text_type, TextType.CODE)
        self.assertIsNone(node.url)

    def test_init_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        self.assertEqual(node.text, "Italic text")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertIsNone(node.url)

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


if __name__ == "__main__":
    unittest.main()
