import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        link = HTMLNode("a", "this is a link", props={"href": "https://www.google.com", "target":"_blank"})
        test_answer = "href=\"https://www.google.com\" target=\"_blank\" "
        self.assertTrue(link.props_to_html() == test_answer)

if __name__ == "__main__":
    unittest.main()