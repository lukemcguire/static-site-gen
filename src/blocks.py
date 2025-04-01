"""Functions for handling block-level markdown."""

from __future__ import annotations

import re
from enum import Enum, auto

from htmlnode import HTMLNode
from parentnode import ParentNode
from parsing import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    """Enumeration of different types of Markdown blocks.

    This enum represents the different types of blocks that can be found
    in Markdown text, such as paragraphs, headings, code blocks, quotes,
    and lists.

    Attributes:
        PARAGRAPH: Represents a standard paragraph of text.
        HEADING: Represents a heading (e.g., # Heading, ## Subheading).
        CODE: Represents a code block (e.g., ```code```).
        QUOTE: Represents a block quote (e.g., > Quote).
        UNORDERED_LIST: Represents an unordered list (e.g., - Item).
        ORDERED_LIST: Represents an ordered list (e.g., 1. Item).
    """

    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown: str) -> list[str]:
    r"""Splits a Markdown string into a list of blocks.

    This function takes a Markdown string as input and splits it into a list
    of blocks based on double newline characters ("\n\n"). It also removes
    leading and trailing whitespace from each block and filters out any empty
    blocks.

    Args:
        markdown: The Markdown string to split into blocks.

    Returns:
        A list of strings, where each string is a block of Markdown text.
        Empty blocks are filtered out.
    """
    blocks = list(filter(lambda x: x != "", (map(str.strip, markdown.split("\n\n")))))
    # blocks = markdown.split("\n\n")
    # blocks = map(str.strip, block)
    # blocks = filter(lambda x: x != "", blocks)
    # blocks = list(blocks)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    """Determines the BlockType of a given Markdown block.

    This function analyzes a Markdown block and determines its type based on
    its content and formatting. It checks for headings, code blocks,
    quotes, unordered lists, and ordered lists. If none of these types
    are detected, it defaults to a paragraph.

    Args:
        block: The Markdown block string to analyze.

    Returns:
        The BlockType of the given block.
    """
    if re.match(
        r"(?P<level>#{1,6})\s+(?P<text>.*)$", block, re.DOTALL | re.MULTILINE
    ):  # extra information in case I need it later.
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Converts a markdown string to a ParentNode.

    This function takes a markdown string, splits it into blocks,
    determines the type of each block, and converts each block
    into a ParentNode.

    Args:
        markdown: The markdown string to convert.

    Returns:
        A ParentNode representing the parsed markdown.

    Raises:
        ValueError: If the block type is invalid.
    """
    children: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(block_to_heading(block))
            case BlockType.CODE:
                children.append(block_to_code(block))
            case BlockType.QUOTE:
                children.append(block_to_quote(block))
            case BlockType.UNORDERED_LIST:
                children.append(block_to_ul(block))
            case BlockType.ORDERED_LIST:
                children.append(block_to_ol(block))
            case BlockType.PARAGRAPH:
                children.append(block_to_paragraph(block))
            case _:
                raise ValueError("invalid block type")

    return ParentNode("div", children)


def block_to_heading(block: str) -> ParentNode:
    """Converts a heading block to a ParentNode.

    This function takes a heading block, extracts the heading level and text,
    and converts the text into a list of ParentNodes.

    Args:
        block: The heading block to convert.

    Returns:
        A ParentNode representing the heading.
    """
    match = re.match(r"(?P<level>#{1,6})\s+(?P<text>.*)$", block, re.DOTALL | re.MULTILINE)
    if match is None:
        return ParentNode("h1", list(map(text_node_to_html_node, text_to_textnodes(""))))
    text_nodes = text_to_textnodes(match.group("text"))
    return ParentNode(f"h{len(match.group('level'))}", list(map(text_node_to_html_node, text_nodes)))


def block_to_code(block: str) -> ParentNode:
    """Converts a code block to a ParentNode.

    This function takes a code block, extracts the code, and
    wraps it in <pre><code> tags.

    Args:
        block: The code block to convert.

    Returns:
        A ParentNode representing the code block.
    """
    text = block[3:-3].lstrip("\n")
    raw_text_node = TextNode(text, TextType.TEXT)
    code_node = ParentNode("code", [text_node_to_html_node(raw_text_node)])
    print(f"code_node : {code_node}")
    return ParentNode("pre", [code_node])


def block_to_quote(block: str) -> ParentNode:
    """Converts a quote block to a ParentNode.

    This function takes a quote block, extracts the quoted text,
    and wraps it in <blockquote> tags.

    Args:
        block: The quote block to convert.

    Returns:
        A ParentNode representing the quote block.
    """
    match = re.findall(r"^>(.*)$", block, flags=re.MULTILINE)
    text = " ".join(line.strip() for line in match)
    text_nodes = text_to_textnodes(text)
    return ParentNode("blockquote", list(map(text_node_to_html_node, text_nodes)))


def block_to_ul(block: str) -> ParentNode:
    """Converts an unordered list block to a ParentNode.

    This function takes an unordered list block, extracts each list item,
    and wraps them in <ul><li> tags.

    Args:
        block: The unordered list block to convert.

    Returns:
        A ParentNode representing the unordered list.
    """
    match = re.findall(r"^-\s(.*)$", block, flags=re.MULTILINE)
    list_nodes: list[HTMLNode] = []
    for item in match:
        list_nodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(item)))))
    return ParentNode("ul", list_nodes)


def block_to_ol(block: str) -> ParentNode:
    """Converts an ordered list block to a ParentNode.

    This function takes an ordered list block, extracts each list item,
    and wraps them in <ol><li> tags.

    Args:
        block: The ordered list block to convert.

    Returns:
        A ParentNode representing the ordered list.
    """
    match = re.findall(r"^\d+\.\s(.*)$", block, flags=re.MULTILINE)
    list_nodes: list[HTMLNode] = []
    for item in match:
        list_nodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(item)))))
    return ParentNode("ol", list_nodes)


def block_to_paragraph(block: str) -> ParentNode:
    """Converts a paragraph block to a ParentNode.

    This function takes a paragraph block and wraps it in <p> tags.

    Args:
        block: The paragraph block to convert.

    Returns:
        A ParentNode representing the paragraph.
    """
    text = " ".join(block.split("\n"))
    return ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(text))))
