import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node, split_nodes_delimiter
from textnode import extract_markdown_images, extract_markdown_links
from textnode import split_nodes_image, split_nodes_link
from textnode import text_to_textnodes
from textnode import markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("Plain", TextType.TEXT, None)
        node2 = TextNode("Plain", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_node_dif(self):
        node = TextNode("This is a link", TextType.LINK, "WWW.youtube.com")
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

class TestTextNodetoHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print(\"Hello World\")", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print(\"Hello World\")")

    def test_link(self):
        node = TextNode("youtube", TextType.LINK, "www.youtube.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "youtube")
        self.assertEqual(html_node.props, {"href": "www.youtube.com"})
    
    def test_image(self):
        node = TextNode("dog", TextType.IMAGE, "dog.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "dog")
        self.assertEqual(html_node.props["src"], "dog.png")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, answer)

    def test_text_with_multiple_bold_words_seperate(self):
        node = TextNode("This is a **text** with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        answer = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, answer)

    def test_text_with_bold_and_italic(self):
        node = TextNode("This is **text** with a _bold_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        answer = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, answer)

    def test_text_with_multiple_bold_words_together(self):
        node = TextNode("This is a **very long** sentence", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        answer = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("very long", TextType.BOLD),
            TextNode(" sentence", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, answer)

    def test_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        answer = [TextNode("", TextType.TEXT)]

        self.assertEqual(new_nodes, answer)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("Guess what you just got ![rick roll](https://i.imgur.com/aKaOqIh.gif) Ricked Rolled")

        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images("We have a ![cat](cat.png) and a ![dog](dog.png)")

        self.assertEqual(matches, [
            ("cat", "cat.png"),
            ("dog", "dog.png"),
        ])

    def test_extract_incomplete_markdown_images(self):
        matches = extract_markdown_images("we have a [cat](cat.png)")

        self.assertEqual(matches, [])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("Guess what you just got [to youtube](www.youtube.com) Ricked Rolled")

        self.assertEqual(matches, [("to youtube", "www.youtube.com")])

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links("We have a [cat](www.cat.org) and a [dog](www.dog.org)")

        self.assertEqual(matches, [
            ("cat", "www.cat.org"),
            ("dog", "www.dog.org"),
        ])

    def test_extract_incomplete_markdown_links(self):
        matches = extract_markdown_links("we have a [cat]cat.png)")

        self.assertEqual(matches, [])

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "This is a text with one image ![dog](dog.png)", TextType.TEXT
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with one image ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "dog.png")
            ],
            new_nodes 
        )

    def test_split_images_none(self):
        node = TextNode("This is a text node", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(new_nodes, [TextNode("This is a text node", TextType.TEXT)])

    def test_split_links(self):
        node = TextNode("This is a text with a link [youtube](www.youtube.com) and [twitch](www.twitch.com)",
                        TextType.TEXT)
        
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is a text with a link ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "www.youtube.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("twitch", TextType.LINK, "www.twitch.com"),
            ],
            new_nodes
        )

    def test_split_link_single(self):
        node = TextNode("This is a text with one link [youtube](www.youtube.com)", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is a text with one link ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "www.youtube.com"),
            ],
            new_nodes
        )

    def test_split_link_none(self):
        node = TextNode("This has no link", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("This has no link", TextType.TEXT)], new_nodes
        )

    def test_split_link_and_image(self):
        node = TextNode("This has both a link [youtube](www.youtube.com) and image ![dog](dog.png)",
                        TextType.TEXT)
        
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)

        self.assertListEqual(
            [
                TextNode("This has both a link ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "www.youtube.com"),
                TextNode(" and image ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "dog.png")
            ],
            new_nodes
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)

        answer = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(new_nodes, answer)

    def test_text_to_text_nodes_only_text(self):
        text = "This is only one piece of text"

        new_nodes = text_to_textnodes(text)

        answer = [
            TextNode("This is only one piece of text", TextType.TEXT)
        ]

        self.assertListEqual(answer, new_nodes)

    def test_text_to_text_nodes_no_words(self):
        text = ""

        new_nodes = text_to_textnodes(text)

        answer = [
            TextNode("", TextType.TEXT)
        ]

        self.assertListEqual(answer, new_nodes)

    def test_text_to_text_nodes_incomplete_markdown(self):
        text = "This is **piece** of _text with no images or links"

        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertEqual(context.exception.args[0], "Invalid Markdown, format is not closed")

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_block(self):
        text = (
            """
            # This is a heading

            This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
            """)

        blocks = markdown_to_blocks(text)

        answer = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
        ]

        self.assertListEqual(answer, blocks)

    def test_markdown_with_list_to_block(self):
        text = (
            """
            # This is a heading

            - This is the first item in a list block
            - This is a list item
            - This is another list item
            """
        )

        blocks = markdown_to_blocks(text)

        answer = [
            "# This is a heading",
            """- This is the first item in a list block
            - This is a list item
            - This is another list item"""
        ]

        self.assertListEqual(answer, blocks)



if __name__ == "__main__":
    unittest.main()