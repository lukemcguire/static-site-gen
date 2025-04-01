"""Main entry point for the static site generator.

This module defines the main entry point for the static site generator,
including the `main` function and the `text_node_to_html_node` function.
It handles the conversion of TextNode objects to LeafNode objects,
which represent HTML elements.

Usage: python main.py
"""

from textnode import TextNode, TextType


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
