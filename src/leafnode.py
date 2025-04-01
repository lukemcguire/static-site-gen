"""Module for representing leaf nodes in an HTML document.

This module defines the LeafNode class, which is a subclass of HTMLNode
and represents HTML elements that do not have children (i.e., leaf nodes).
"""

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """Represents a leaf node in an HTML document.

    A leaf node is an HTML element that does not have any child elements.
    It can have a tag, a value, and properties.

    Attributes:
        value (str): The text content of the leaf node.
        tag (str | None): The HTML tag of the leaf node (e.g., "p", "span").
        props (dict[str, str] | None): A dictionary of HTML attributes
            (e.g., {"class": "my-class", "id": "my-id"}).
    """

    def __init__(self, value: str, tag: str | None, props: dict[str, str] | None = None) -> None:
        """Initializes a LeafNode object.

        Args:
            value: The text content of the leaf node.
            tag: The HTML tag of the leaf node.
            props: A dictionary of HTML attributes. Defaults to None.
        """
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __repr__(self) -> str:
        """Returns a string representation of the LeafNode object.

        Returns:
            str: A string representation of the LeafNode object.
        """
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self) -> str:
        """Converts the LeafNode to an HTML string.

        Returns:
            str: The HTML string representation of the leaf node.

        Raises:
            ValueError: If the leaf node does not have a value.
        """
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
