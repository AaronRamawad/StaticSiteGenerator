import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(context.exception.args[0], "Missing Value")

    def test_leaf_to_html_without_tag(self):
        node = LeafNode(tag=None, value="Text")
        test_answer = "Text"
        self.assertEqual(node.to_html(), test_answer)

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_p(self):
        node = ParentNode("p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        test_answer = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), test_answer )

    def test_parent_to_html_p_without_children(self):
        node = ParentNode("p", [])
        test_answer = "<p></p>"
        self.assertEqual(node.to_html(), test_answer)

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        test_answer = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), test_answer)

    def test_parent_to_html_without_tag(self):
        node = ParentNode(tag=None, children=[])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(context.exception.args[0], "Missing Tag")

    def test_parent_to_html_without_children(self):
        node = ParentNode("a", children=None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(context.exception.args[0], "Missing Children")


if __name__ == "__main__":
    unittest.main()