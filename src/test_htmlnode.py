import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_not_implemented(self):
        node = HTMLNode("a", "this is the text of the link", None, {"href": "https://example.org"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode()
        node_repr = repr(node)
        self.assertEqual(
            node_repr,
            'HTMLNode(\n    tag=,\n    value=,\n    children=,\n    props=\n)'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://example.org"})
        self.assertEqual(node.props_to_html(), ' href="https://example.org"')
