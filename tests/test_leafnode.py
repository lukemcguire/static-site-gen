import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("Hello", "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_props(self):
        props = {"class": "my-class", "id": "my-id"}
        node = LeafNode("Hello", "p", props)
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, props)

    def test_to_html_with_tag(self):
        node = LeafNode("Hello", "p")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_no_tag(self):
        node = LeafNode("Hello", None)
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_with_props(self):
        props = {"class": "my-class", "id": "my-id"}
        node = LeafNode("Hello", "p", props)
        self.assertEqual(node.to_html(), '<p class="my-class" id="my-id">Hello</p>')

    def test_to_html_no_value(self):
        node = LeafNode(None, "p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_multiple_props(self):
        props = {"class": "my-class", "id": "my-id", "data-value": "123"}
        node = LeafNode("Hello", "span", props)
        self.assertEqual(node.to_html(), '<span class="my-class" id="my-id" data-value="123">Hello</span>')

    def test_repr(self):
        node = LeafNode("Hello", "p")
        self.assertEqual(repr(node), "LeafNode(p, Hello, None)")

    def test_repr_with_props(self):
        props = {"class": "my-class", "id": "my-id"}
        node = LeafNode("Hello", "p", props)
        self.assertEqual(repr(node), "LeafNode(p, Hello, {'class': 'my-class', 'id': 'my-id'})")


if __name__ == "__main__":
    unittest.main()
