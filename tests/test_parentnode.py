import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_node_initialization(self):
        child1 = LeafNode("Child 1", "p")
        child2 = LeafNode("Child 2", "span")
        children = [child1, child2]
        props = {"class": "container", "id": "main"}
        parent = ParentNode("div", children, props)

        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, children)
        self.assertEqual(parent.props, props)
        self.assertIsNone(parent.value)

    def test_parent_node_to_html_with_children(self):
        child1 = LeafNode("Child 1", "p")
        child2 = LeafNode("Child 2", "span")
        children = [child1, child2]
        parent = ParentNode("div", children)

        expected_html = "<div><p>Child 1</p><span>Child 2</span></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_to_html_with_props(self):
        child1 = LeafNode("Child 1", "p")
        child2 = LeafNode("Child 2", "span")
        children = [child1, child2]
        props = {"class": "container", "id": "main"}
        parent = ParentNode("div", children, props)

        expected_html = '<div class="container" id="main"><p>Child 1</p><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_to_html_no_tag(self):
        child1 = LeafNode("Child 1", "p")
        children = [child1]
        parent = ParentNode(None, children)

        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Parent nodes must have a tag.")

    def test_parent_node_to_html_no_children(self):
        parent = ParentNode("div", None)

        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Parent node missing child nodes.")

    def test_parent_node_to_html_with_leaf_children(self):
        child1 = LeafNode("Child 1", "p")
        child2 = LeafNode("Child 2", "span")
        children = [child1, child2]
        parent = ParentNode("div", children)

        expected_html = "<div><p>Child 1</p><span>Child 2</span></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_to_html_with_nested_parent_children(self):
        grandchild = LeafNode("Grandchild", "p")
        child = ParentNode("section", [grandchild])
        parent = ParentNode("div", [child])

        expected_html = "<div><section><p>Grandchild</p></section></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_repr(self):
        child1 = LeafNode("Child 1", "p")
        child2 = LeafNode("Child 2", "span")
        children = [child1, child2]
        parent = ParentNode("div", children)
        self.assertEqual(repr(parent), "HTMLNode(div, None, 2 child nodes, None)")

    def test_parent_node_repr_with_props(self):
        child1 = LeafNode("Child 1", "p")
        child2 = LeafNode("Child 2", "span")
        children = [child1, child2]
        props = {"class": "container", "id": "main"}
        parent = ParentNode("div", children, props)
        self.assertEqual(repr(parent), "HTMLNode(div, None, 2 child nodes, {'class': 'container', 'id': 'main'})")

    def test_parent_node_init_no_props(self):
        child1 = LeafNode("Child 1", "p")
        child2 = LeafNode("Child 2", "span")
        children = [child1, child2]
        parent = ParentNode("div", children)
        self.assertIsNone(parent.props)


if __name__ == "__main__":
    unittest.main()
