import unittest

from parsing import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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
            TextNode("", TextType.BOLD),  # First ** pair encloses ""
            TextNode("bold", TextType.TEXT),  # Between the middle ** and **
            TextNode("", TextType.BOLD),  # Second ** pair encloses ""
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_no_images(self):
        text = "This is a test with no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_single_image(self):
        text = "![Alt text](https://example.com/image.png)"
        expected = [("Alt text", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![Alt 1](https://example.com/image1.png) Some text ![Alt 2](http://example.com/image2.jpg)"
        expected = [
            ("Alt 1", "https://example.com/image1.png"),
            ("Alt 2", "http://example.com/image2.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_different_protocols(self):
        text = "![Alt text](http://example.com/image.png)"
        expected = [("Alt text", "http://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_text_around(self):
        text = "Some text before ![Alt text](https://example.com/image.png) and after"
        expected = [("Alt text", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_no_links(self):
        text = "This is a test with no links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_single_link(self):
        text = "[Link text](https://example.com)"
        expected = [("Link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[Link 1](https://example.com/1) Some text [Link 2](http://example.com/2)"
        expected = [
            ("Link 1", "https://example.com/1"),
            ("Link 2", "http://example.com/2"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_different_protocols(self):
        text = "[Link text](http://example.com)"
        expected = [("Link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_text_around(self):
        text = "Some text before [Link text](https://example.com) and after"
        expected = [("Link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_ignore_image_syntax(self):
        """Ensure image markdown is not extracted as a link."""
        text = "This is text with an ![image link](https://example.com/img.png) and a [real link](https://example.com)."
        expected = [("real link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_empty_nodes(self):
        nodes = []
        result = split_nodes_image(nodes)
        self.assertEqual(result, [])

    def test_split_image_non_text_nodes_only(self):
        nodes = [TextNode("bold text", TextType.BOLD), TextNode("italic text", TextType.ITALIC)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)

    def test_split_image_single_image(self):
        node = TextNode("Text before ![alt text](https://example.com/img.png) text after", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_image_at_start(self):
        node = TextNode("![alt text](http://example.com/img.png) text after", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("alt text", TextType.IMAGE, "http://example.com/img.png"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_image_at_end(self):
        node = TextNode("Text before ![alt text](https://example.com/img.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_split_image_multiple_images(self):
        node = TextNode(
            "Image 1: ![alt1](https://url1.com/a.jpg) and Image 2: ![alt2](http://url2.org/b.png) end.", TextType.TEXT
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Image 1: ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "https://url1.com/a.jpg"),
            TextNode(" and Image 2: ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "http://url2.org/b.png"),
            TextNode(" end.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_image_adjacent_images(self):
        node = TextNode("Before ![alt1](https://url1.com)![alt2](http://url2.net) After", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "https://url1.com"),
            TextNode("alt2", TextType.IMAGE, "http://url2.net"),
            TextNode(" After", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_image_multiple_nodes_mixed(self):
        nodes = [
            TextNode("Node 1 with ![img1](https://url1.com)", TextType.TEXT),
            TextNode("Node 2 is plain text.", TextType.TEXT),
            TextNode("Node 3 ![img2](http://url2.com) end", TextType.TEXT),
            TextNode("Node 4 is bold", TextType.BOLD),
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Node 1 with ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://url1.com"),
            TextNode("Node 2 is plain text.", TextType.TEXT),
            TextNode("Node 3 ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "http://url2.com"),
            TextNode(" end", TextType.TEXT),
            TextNode("Node 4 is bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_split_image_ignores_links(self):
        node = TextNode("Text with a [link](https://link.com) and ![image](http://image.org).", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with a [link](https://link.com) and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "http://image.org"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_link_empty_nodes(self):
        nodes = []
        result = split_nodes_link(nodes)
        self.assertEqual(result, [])

    def test_split_link_non_text_nodes_only(self):
        nodes = [TextNode("bold text", TextType.BOLD), TextNode("italic text", TextType.ITALIC)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)

    def test_split_link_single_link(self):
        node = TextNode("Text before [anchor text](https://example.com) text after", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "https://example.com"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_link_at_start(self):
        node = TextNode("[anchor text](http://example.com) text after", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("anchor text", TextType.LINK, "http://example.com"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_link_at_end(self):
        node = TextNode("Text before [anchor text](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_split_link_multiple_links(self):
        node = TextNode(
            "Link 1: [anchor1](https://url1.com) and Link 2: [anchor2](http://url2.org) end.", TextType.TEXT
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Link 1: ", TextType.TEXT),
            TextNode("anchor1", TextType.LINK, "https://url1.com"),
            TextNode(" and Link 2: ", TextType.TEXT),
            TextNode("anchor2", TextType.LINK, "http://url2.org"),
            TextNode(" end.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_link_adjacent_links(self):
        node = TextNode("Before [a1](https://u1.com)[a2](http://u2.net) After", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("a1", TextType.LINK, "https://u1.com"),
            TextNode("a2", TextType.LINK, "http://u2.net"),
            TextNode(" After", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_link_multiple_nodes_mixed(self):
        nodes = [
            TextNode("Node 1 with [link1](https://url1.com)", TextType.TEXT),
            TextNode("Node 2 is plain text.", TextType.TEXT),
            TextNode("Node 3 [link2](http://url2.com) end", TextType.TEXT),
            TextNode("Node 4 is image", TextType.IMAGE, "https://img.url"),
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Node 1 with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://url1.com"),
            TextNode("Node 2 is plain text.", TextType.TEXT),
            TextNode("Node 3 ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "http://url2.com"),
            TextNode(" end", TextType.TEXT),
            TextNode("Node 4 is image", TextType.IMAGE, "https://img.url"),
        ]
        self.assertEqual(result, expected)

    def test_split_link_ignores_images(self):
        node = TextNode("Text with ![image](https://image.org) and a [link](http://link.com).", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text with ![image](https://image.org) and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://link.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text with no markdown."
        result = text_to_textnodes(text)
        expected = [TextNode("This is plain text with no markdown.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_only_bold(self):
        text = "Text with **bold content** here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold content", TextType.BOLD),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_only_italic_asterisk(self):
        text = "Text with *italic content* here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("italic content", TextType.ITALIC),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_only_italic_underscore(self):
        text = "Text with _italic content_ here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("italic content", TextType.ITALIC),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_only_code(self):
        text = "Text with `code content` here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code content", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_only_image(self):
        text = "Text with ![alt text](https://image.com/pic.png) here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://image.com/pic.png"),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_only_link(self):
        text = "Text with [anchor text](http://link.com/page) here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "http://link.com/page"),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        text = (
            "This is **bold** and *italic* with `code` and an ![image](https://img.url) and a [link](http://lnk.url)."
        )
        result = text_to_textnodes(text)
        # Expected order based on function logic: **, _, *, `, image, link
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://img.url"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://lnk.url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    # Nested delimiters not currently implemented
    # def test_italic_within_bold(self):
    #     # Note: The current implementation processes delimiters sequentially.
    #     # '**' is processed first, then '*'
    #     text = "This is **bold with *italic* inside** text."
    #     result = text_to_textnodes(text)
    #     # After **: [TextNode("This is ", T), TextNode("bold with *italic* inside", B), TextNode(" text.", T)]
    #     # After *:  [TextNode("This is ", T), TextNode("bold with ", B), TextNode("italic", I), TextNode(" inside", B), TextNode(" text.", T)]
    #     # Final node list should reflect the splits
    #     expected = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("bold with ", TextType.BOLD),
    #         TextNode("italic", TextType.ITALIC),
    #         TextNode(" inside", TextType.BOLD),
    #         TextNode(" text.", TextType.TEXT),
    #     ]
    #     self.assertEqual(result, expected)

    # def test_bold_within_italic(self):
    #     # '*' processed after '**'.
    #     text = "This is *italic with **bold** inside* text."
    #     result = text_to_textnodes(text)
    #     # After **: [TextNode("This is *italic with ", T), TextNode("bold", B), TextNode(" inside* text.", T)]
    #     # After *:  [TextNode("This is ", T), TextNode("italic with ", I), TextNode("bold", B), TextNode(" inside", I), TextNode(" text.", T)]
    #     expected = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("italic with ", TextType.ITALIC),
    #         TextNode("bold", TextType.BOLD),
    #         TextNode(" inside", TextType.ITALIC),
    #         TextNode(" text.", TextType.TEXT),
    #     ]
    #     self.assertEqual(result, expected)

    def test_image_and_link_together(self):
        text = "An ![image](https://img.url) followed by a [link](http://lnk.url)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://img.url"),
            TextNode(" followed by a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://lnk.url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_input(self):
        text = ""
        result = text_to_textnodes(text)
        # Starts with [TextNode("", TEXT)], no splits change it
        expected = [TextNode("", TextType.TEXT)]
        # Filter out empty text nodes if the implementation detail changes
        # result_filtered = [node for node in result if node.text or node.text_type != TextType.TEXT]
        # expected_filtered = []
        # self.assertEqual(result_filtered, expected_filtered)
        # For now, test the actual output:
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises_exception(self):
        text = "This has an **unmatched delimiter"
        with self.assertRaises(Exception) as context:
            text_to_textnodes(text)
        self.assertIn("Unmatched ** delimiter", str(context.exception))


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid(self):
        markdown = "# My Page Title\nSome other content"
        self.assertEqual(extract_title(markdown), "My Page Title")

    def test_extract_title_no_title(self):
        markdown = "Some content without a title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "markdown does not contain h1 title")

    def test_extract_title_multiple_titles(self):
        markdown = "# My Page Title\n# Another Title"
        self.assertEqual(extract_title(markdown), "My Page Title")


if __name__ == "__main__":
    unittest.main()
