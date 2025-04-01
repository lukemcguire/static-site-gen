"""Main entry point for the static site generator.

This module defines the main entry point for the static site generator,
including the `main` function and the `text_node_to_html_node` function.
It handles the conversion of TextNode objects to LeafNode objects,
which represent HTML elements.

Usage: python main.py
"""

import re

from blocks import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from parsing import text_to_textnodes
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Converts a TextNode object to a LeafNode object.

    This function takes a TextNode object and converts it into a LeafNode
    object, which represents an HTML element. The type of the TextNode
    determines the HTML tag and properties of the resulting LeafNode.

    Args:
        text_node: The TextNode object to convert.

    Returns:
        A LeafNode object representing the HTML element.

    Raises:
        Exception: If the TextNode has an unknown text type.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text, None)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            url = text_node.url if text_node.url is not None else ""
            props = {"href": url}
            return LeafNode(text_node.text, "a", props)
        case TextType.IMAGE:
            url = text_node.url if text_node.url is not None else ""
            alt_text = text_node.text if text_node.text is not None else ""
            props = {"src": url, "alt": alt_text}
            return LeafNode("", "img", props)
        case _:
            raise Exception("Unknown text type.")


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Converts a markdown string to a ParentNode.

    This function takes a markdown string, splits it into blocks,
    determines the type of each block, and converts each block
    into a ParentNode.

    Args:
        markdown: The markdown string to convert.

    Returns:
        A ParentNode representing the parsed markdown.
    """
    nodes: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                nodes.append(block_to_heading(block))
            case BlockType.CODE:
                nodes.append(block_to_code(block))
            case BlockType.QUOTE:
                nodes.append(block_to_quote(block))
            case BlockType.UNORDERED_LIST:
                nodes.append(block_to_ul(block))
            case BlockType.ORDERED_LIST:
                nodes.append(block_to_ol(block))
            case BlockType.PARAGRAPH:
                nodes.append(block_to_paragraph(block))

    return ParentNode("div", nodes)


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
    code_node = LeafNode(text, "code")
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
    return ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(block))))


def main() -> None:
    """Entry point for the static site generator.

    This function serves as the main entry point for the static site
    generator. Currently, it demonstrates the creation of a TextNode
    and prints its representation. In the future, it will orchestrate
    the entire site generation process.
    """
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
