"""Module for representing HTML nodes in a document.

This module defines the HTMLNode class, which is used to represent
different HTML elements and their associated properties, such as
tags, values, children, and attributes.
"""


class HTMLNode:
    """Represents a node in an HTML document.

    Attributes:
        tag (str | None): The HTML tag of the node (e.g., "div", "p").
        value (str | None): The text content of the node.
        children (list[HTMLNode] | None): A list of child HTMLNode objects.
        props (dict[str, str] | None): A dictionary of HTML attributes
            (e.g., {"class": "my-class", "id": "my-id"}).
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        """Initializes an HTMLNode object.

        Args:
            tag: The HTML tag of the node. Defaults to None.
            value: The text content of the node. Defaults to None.
            children: A list of child HTMLNode objects. Defaults to None.
            props: A dictionary of HTML attributes. Defaults to None.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        """Returns a string representation of the HTMLNode object.

        Returns:
            str: A string representation of the HTMLNode object.
        """
        num_children = 0 if self.children is None else len(self.children)
        return f"HTMLNode({self.tag}, {self.value}, {num_children} child nodes, {self.props})"

    def to_html(self) -> str:
        """Converts the HTMLNode to an HTML string.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Returns:
            str: The HTML string representation of the node.
        """
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Converts the node's properties to an HTML attribute string.

        Returns:
            str: An HTML attribute string (e.g., ' class="my-class" id="my-id"').
                Returns an empty string if there are no properties.
        """
        if self.props is None:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
