import unittest

from parsing import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty_nodes(self):
        """Test splitting an empty list of nodes."""
        nodes = []
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_no_delimiter(self):
        """Test splitting nodes with no delimiter present."""
        nodes = [TextNode("This is a test", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("This is a test", TextType.TEXT)])

    def test_bold_single_delimiter_odd(self):
        """Test splitting nodes with an odd number of bold delimiters."""
        nodes = [TextNode("This is **a test", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid Markdown: Unmatched ** delimiter.")

    def test_bold_single_delimiter_even(self):
        """Test splitting nodes with an even number of bold delimiters."""
        nodes = [TextNode("This is **a** test", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a", TextType.BOLD),
            TextNode(" test", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold_multiple_delimiters(self):
        """Test splitting nodes with multiple bold delimiters."""
        nodes = [TextNode("This is **a** test **with** multiple delimiters", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a", TextType.BOLD),
            TextNode(" test ", TextType.TEXT),
            TextNode("with", TextType.BOLD),
            TextNode(" multiple delimiters", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold_multiple_nodes(self):
        """Test splitting multiple nodes, some with bold delimiters."""
        nodes = [
            TextNode("This is **a** test", TextType.TEXT),
            TextNode("Another test", TextType.TEXT),
            TextNode("And **another** one", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a", TextType.BOLD),
            TextNode(" test", TextType.TEXT),
            TextNode("Another test", TextType.TEXT),
            TextNode("And ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
            TextNode(" one", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_single_delimiter_odd_underscore(self):
        """Test splitting nodes with an odd number of italic delimiters (underscore)."""
        nodes = [TextNode("This is _a test", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Invalid Markdown: Unmatched _ delimiter.")

    def test_italic_single_delimiter_even_underscore(self):
        """Test splitting nodes with an even number of italic delimiters (underscore)."""
        nodes = [TextNode("This is _a_ test", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a", TextType.ITALIC),
            TextNode(" test", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_single_delimiter_odd_asterisk(self):
        """Test splitting nodes with an odd number of italic delimiters (asterisk)."""
        nodes = [TextNode("This is *a test", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Invalid Markdown: Unmatched * delimiter.")

    def test_italic_single_delimiter_even_asterisk(self):
        """Test splitting nodes with an even number of italic delimiters (asterisk)."""
        nodes = [TextNode("This is *a* test", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a", TextType.ITALIC),
            TextNode(" test", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_single_delimiter_odd(self):
        """Test splitting nodes with an odd number of code delimiters."""
        nodes = [TextNode("This is `a test", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid Markdown: Unmatched ` delimiter.")

    def test_code_single_delimiter_even(self):
        """Test splitting nodes with an even number of code delimiters."""
        nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_type_nodes(self):
        """Test splitting nodes with non-TEXT type nodes."""
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text **with** delimiters", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text ", TextType.TEXT),
            TextNode("with", TextType.BOLD),
            TextNode(" delimiters", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_start_and_end(self):
        """Test splitting nodes with delimiters at the start and end."""
        nodes = [TextNode("**bold**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters_in_a_row(self):
        """Test splitting nodes with multiple delimiters in a row."""
        nodes = [TextNode("This is ****bold**** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode("bold", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
