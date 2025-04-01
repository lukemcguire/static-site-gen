"""Module for representing text nodes in a document.

This module defines the TextType enum and the TextNode class, which are used to
represent different types of text and their associated properties, such as
links.
"""

from __future__ import annotations

from enum import Enum, auto

from leafnode import LeafNode


class TextType(Enum):
    """Enumeration of different text types.

    Attributes:
        NORMAL: Represents normal text.
        BOLD: Represents bold text.
        ITALIC: Represents italic text.
        CODE: Represents code text.
        LINKS: Represents text that is a link.
        IMAGES: Represents text that is an image.
    """

    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()


class TextNode:
    """Represents a node of text with a specific type and optional URL.

    Attributes:
        text: The text content of the node.
        text_type: The type of the text (e.g., normal, bold, link).
        url: An optional URL associated with the text (e.g., for links).
    """

    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        """Initializes a TextNode object.

        Args:
            text: The text content of the node.
            text_type: The type of the text.
            url: An optional URL associated with the text.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        """Checks if two TextNode objects are equal.

        Args:
            other: The other TextNode object to compare to.

        Returns:
            True if the two TextNode objects are equal, False otherwise.
        """
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        """Returns a string representation of the TextNode object.

        Returns:
            A string representation of the TextNode object.
        """
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"


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
