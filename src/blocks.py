"""Functions for handling block-level markdown."""

from __future__ import annotations

import re
from enum import Enum, auto


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
