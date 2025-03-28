"""Text parsing utility functions."""

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
