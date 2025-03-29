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


def split_nodes_link(old_nodes: list["TextNode"]) -> list["TextNode"]:
    """Splits a list of TextNodes based on Markdown link syntax.

    This function takes a list of TextNodes and splits any TextNodes with
    `TextType.TEXT` into multiple nodes based on the presence of Markdown
    links (`[anchor text](URL)`). Text before, between, and after links
    remains `TextType.TEXT`, while the link text is converted to
    `TextType.LINK` with the corresponding URL.

    Args:
        old_nodes: A list of TextNode objects to be parsed.

    Returns:
        A new list of TextNode objects with the text split and links
        converted to `TextType.LINK`.
    """
    parsed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            parsed_nodes.append(node)
            continue
        new_nodes = []
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            parsed_nodes.append(TextNode(text, TextType.TEXT))
            continue
        for anchor_text, link_url in links:
            before, after = text.split(f"[{anchor_text}]({link_url})", 1)
            if len(before) > 0:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))
            text = after
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

        parsed_nodes.extend(new_nodes)
    return parsed_nodes


def split_nodes_image(old_nodes: list["TextNode"]) -> list["TextNode"]:
    """Splits a list of TextNodes based on Markdown image syntax.

    This function takes a list of TextNodes and splits any TextNodes with
    `TextType.TEXT` into multiple nodes based on the presence of Markdown
    images (`![alt text](URL)`). Text before, between, and after images
    remains `TextType.TEXT`, while the image alt text is converted to
    `TextType.IMAGE` with the corresponding URL.

    Args:
        old_nodes: A list of TextNode objects to be parsed.

    Returns:
        A new list of TextNode objects with the text split and images
        converted to `TextType.IMAGE`.
    """
    parsed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            parsed_nodes.append(node)
            continue
        new_nodes = []
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            parsed_nodes.append(TextNode(text, TextType.TEXT))
            continue
        for alt_text, image_url in images:
            before, after = text.split(f"![{alt_text}]({image_url})", 1)
            if len(before) > 0:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            text = after
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

        parsed_nodes.extend(new_nodes)
    return parsed_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extracts image information from Markdown text.

    This function searches the input string for Markdown image syntax
    `!alt text` and extracts the alt text and URL.

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
    `anchor text` and extracts the anchor text and URL. It will not
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


def text_to_textnodes(text: str) -> list["TextNode"]:
    """Converts a string of text into a list of TextNodes.

    This function takes a string of text and parses it, identifying
    various Markdown elements such as bold, italic, code, links, and
    images. It then converts these elements into a list of TextNode
    objects, each representing a segment of the original text with
    its corresponding type and any associated data (e.g., URLs for
    links and images).

    Args:
        text: The input string of text to be parsed.

    Returns:
        A list of TextNode objects representing the parsed text.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = ("**", "_", "*", "`")
    text_types = (TextType.BOLD, TextType.ITALIC, TextType.ITALIC, TextType.CODE)
    for delimiter, text_type in zip(delimiters, text_types, strict=False):
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
