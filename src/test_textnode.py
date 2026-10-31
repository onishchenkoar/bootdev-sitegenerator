import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_empty_url_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node)[-3:], ", )")

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALICS)
        self.assertNotEqual(node, node2)

    def test_dummy(self):
        self.assertEqual(1, 1)



if __name__ == "__main__":
    unittest.main()
