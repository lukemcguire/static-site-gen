import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_no_args(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_args(self):
        children = [HTMLNode("p", "Child 1"), HTMLNode("p", "Child 2")]
        props = {"class": "my-class", "id": "my-id"}
        node = HTMLNode("div", "Some text", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Some text")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].value, "Child 1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[1].value, "Child 2")
        self.assertEqual(node.props, props)

    def test_repr_no_args(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, 0 child nodes, None)")

    def test_repr_with_args(self):
        children = [HTMLNode("p", "Child 1"), HTMLNode("p", "Child 2")]
        props = {"class": "my-class", "id": "my-id"}
        node = HTMLNode("div", "Some text", children, props)
        self.assertEqual(
            repr(node),
            "HTMLNode(div, Some text, 2 child nodes, {'class': 'my-class', 'id': 'my-id'})",
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        props = {"class": "my-class", "id": "my-id", "data-value": "123"}
        node = HTMLNode(props=props)
        expected = ' class="my-class" id="my-id" data-value="123"'
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
