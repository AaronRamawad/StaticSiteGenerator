import unittest

from textnode import TextNode, TextType 

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("Plain", TextType.TEXT, None)
        node2 = TextNode("Plain", TextType.TEXT)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()