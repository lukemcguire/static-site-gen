import unittest
from enum import Enum, auto

from main import text_node_to_html_node
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


if __name__ == "__main__":
    unittest.main()
