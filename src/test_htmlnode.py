import unittest
from htmlnode import HTMLNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_a(self):
        link = HTMLNode("a", "this is a link", props={"href": "https://www.google.com", "target":"_blank"})
        test_answer = "href=\"https://www.google.com\" target=\"_blank\""
        self.assertTrue(link.props_to_html() == test_answer)

    def test_props_to_html_no_props(self):
        link = HTMLNode("a", "this is a link")
        test_answer = ""
        self.assertEqual(link.props_to_html(), test_answer)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        test_answer = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), test_answer)

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Youtube", {"href": "https://www.youtube.com"})
        test_answer = "<a href=\"https://www.youtube.com\">Youtube</a>"
        self.assertEqual(node.to_html(), test_answer)

    def test_leaf_to_html_without_value(self):
        node = LeafNode("p", value=None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_without_tag(self):
        node = LeafNode(tag=None, value="Text")
        test_answer = "Text"
        self.assertEqual(node.to_html(), test_answer)
        

if __name__ == "__main__":
    unittest.main()