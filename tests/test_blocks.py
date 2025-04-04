import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_paragraphs(self):
        md = """
Paragraph 1

Paragraph 2

Paragraph 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph 1", "Paragraph 2", "Paragraph 3"])

    def test_leading_and_trailing_whitespace(self):
        md = """
   Paragraph 1 

  Paragraph 2  
"""  # noqa: W291
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph 1", "Paragraph 2"])

    def test_empty_paragraphs(self):
        md = """
Paragraph 1


Paragraph 2


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph 1", "Paragraph 2"])

    def test_mixed_content(self):
        md = """
# Heading 1

This is a paragraph with **bold** text.

- List item 1
- List item 2

## Heading 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# Heading 1", "This is a paragraph with **bold** text.", "- List item 1\n- List item 2", "## Heading 2"],
        )

    def test_only_whitespace(self):
        md = "   \n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_line_break(self):
        md = "This is a single line\nThis is the second line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line\nThis is the second line"])

    def test_multiple_line_breaks(self):
        md = """
This is a paragraph with a line break
in the middle

This is another paragraph
with a line break
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is a paragraph with a line break\nin the middle", "This is another paragraph\nwith a line break"],
        )


# This is not implemented correctly yet. Need to decide how we want to handle cases like this
#
#     def test_multiple_headings(self):
#         md = """
# # Heading 1
# ## Heading 2
# ### Heading 3
# """
#         blocks = markdown_to_blocks(md)
#         self.assertEqual(blocks, ["# Heading 1", "## Heading 2", "### Heading 3"])


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_level_1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_2(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nCode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_content(self):
        block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_multiline_quote(self):
        block = """> This is a
> multiline quote."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        block = "- Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        block = "1. Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_non_sequential(self):
        block = "1. Item 1\n3. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### Heading 7"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_mixed_content(self):
        block = "- Item 1\nThis is not a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_mixed_content(self):
        block = "1. Item 1\nThis is not a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_mixed_content(self):
        block = """> This is a quote.
This is not a quote."""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_no_content(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_no_ending(self):
        block = "```\nprint('Hello, world!')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_no_beginning(self):
        block = "print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

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

    def test_markdown_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_markdown_ordered_list(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>")

    def test_markdown_quote(self):
        md = """> This is a quote
> with multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote with multiple lines</blockquote></div>")


if __name__ == "__main__":
    unittest.main()
