import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "this is the text of the link", {"href": "https://example.org"})
        self.assertEqual(node.to_html(), '<a href="https://example.org">this is the text of the link</a>')


    def test_repr(self):
        node = LeafNode("", "")
        node_repr = repr(node)
        self.assertEqual(
            node_repr,
            'LeafNode(\n    tag=,\n    value=,\n    props=\n)'
        )

    def test_init(self):
        with self.assertRaises(TypeError):
            node = LeafNode()
