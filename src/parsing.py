"""Text parsing utility functions."""

import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list["TextNode"], delimiter: str, text_type: TextType) -> list["TextNode"]:
    """Splits a list of TextNodes based on a delimiter and assigns a new TextType.

    This function takes a list of TextNodes and splits any TextNodes with
    `TextType.TEXT` into multiple nodes based on the provided delimiter.
    Text between delimiters is assigned the specified `text_type`, while text
    outside delimiters remains `TextType.TEXT`.

    Args:
        old_nodes: A list of TextNode objects to be parsed.
        delimiter: The delimiter string used to split the text.
        text_type: The TextType to assign to text between delimiters.

    Returns:
        A new list of TextNode objects with the text split and new types assigned.

    Raises:
        Exception: If an odd number of delimiters is found in a TextNode's text,
            indicating unmatched delimiters.
    """
    parsed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            parsed_nodes.append(node)
            continue
        new_nodes = []
        text = node.text
        if text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid Markdown: Unmatched {delimiter} delimiter.")
        chunks = text.split(delimiter)
        for i, chunk in enumerate(chunks):
            if i % 2 == 0:
                new_nodes.append(TextNode(chunk, TextType.TEXT))
            else:
                new_nodes.append(TextNode(chunk, text_type))

        parsed_nodes.extend(new_nodes)
    return parsed_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extracts image information from Markdown text.

    This function searches the input string for Markdown image syntax
    `![alt text](URL)` and extracts the alt text and URL.

    Args:
        text: The Markdown text to search.

    Returns:
        A list of tuples, where each tuple contains the alt text and the URL
        of an image found in the text. If no images are found, returns an
        empty list.
        For example: [("alt text", "https://example.com/image.png")]
    """
    return re.findall(r"!\[(.*?)\]\((https?:\/\/.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extracts link information from Markdown text.

    This function searches the input string for Markdown link syntax
    `[anchor text](URL)` and extracts the anchor text and URL. It will not
    extract links that are part of an image.

    Args:
        text: The Markdown text to search.

    Returns:
        A list of tuples, where each tuple contains the anchor text and the
        URL of a link found in the text. If no links are found, returns an
        empty list.
        For example: [("anchor text", "https://example.com")]
    """
    return re.findall(r"(?<!!)\[(.*?)\]\((https?:\/\/.*?)\)", text)
