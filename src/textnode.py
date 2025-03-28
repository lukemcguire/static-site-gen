"""Module for representing text nodes in a document.

This module defines the TextType enum and the TextNode class, which are used to
represent different types of text and their associated properties, such as
links.
"""

from __future__ import annotations

from enum import Enum, auto


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

    NORMAL = auto()
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
