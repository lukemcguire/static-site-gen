"""Main entry point for the static site generator.

Usage: python main.py
"""

from textnode import TextNode, TextType


def main() -> None:
    """Make a jazz noise here."""
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
