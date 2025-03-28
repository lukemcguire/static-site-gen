"""Main entry point for the static site generator.

This module defines the main entry point for the static site generator,
including the `main` function and the `text_node_to_html_node` function.
It handles the conversion of TextNode objects to LeafNode objects,
which represent HTML elements.

Usage: python main.py
"""

from textnode import TextNode, TextType
from leafnode import LeafNode


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
        case TextType.NORMAL:
            return LeafNode(text_node.text, None)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            props = {"href": text_node.url}
            return LeafNode(text_node.text, "a", props)
        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode("", "img", props)
        case _:
            raise Exception("Unknown text type.")


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
