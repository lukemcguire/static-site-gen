"""Module for representing parent nodes in an HTML document.

This module defines the ParentNode class, which is a subclass of HTMLNode
and represents HTML elements that can have child elements.
"""

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """Represents a parent node in an HTML document.

    A parent node is an HTML element that can contain other HTML elements
    as children. It has a tag, a list of children, and optional properties.

    Attributes:
        tag (str): The HTML tag of the parent node (e.g., "div", "body").
        children (list[HTMLNode]): A list of child HTMLNode objects.
        props (dict[str, str] | None): A dictionary of HTML attributes
            (e.g., {"class": "my-class", "id": "my-id"}).
    """

    def __init__(self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None) -> None:
        """Initializes a ParentNode object.

        Args:
            tag: The HTML tag of the parent node.
            children: A list of child HTMLNode objects.
            props: A dictionary of HTML attributes. Defaults to None.
        """
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __repr__(self) -> str:
        """Returns a string representation of the ParentNode object.

        Returns:
            str: A string representation of the ParentNode object.
        """
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self) -> str:
        """Converts the ParentNode to an HTML string.

        Returns:
            str: The HTML string representation of the parent node,
                including its children.

        Raises:
            ValueError: If the parent node does not have a tag.
            ValueError: If the parent node is missing child nodes.
        """
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("Parent node missing child nodes.")
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
