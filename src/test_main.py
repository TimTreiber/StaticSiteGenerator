import unittest

from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
from main import *

class TestTextNode(unittest.TestCase):
    def test_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        node3 = TextNode("This is an image node", TextType.IMAGE, "www.gidf.com")
        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is a bold node")
        self.assertEqual(html_node3.props_to_html(), ' src="www.gidf.com" alt="This is an image node"')

    def test_delimiter_splitting(self):
        newNode = TextNode("This is some `code block` blabla. Here is some **bold text** followed by _italic text_ and nothing else!", "text")
        new_list = split_nodes_delimiter([newNode], "`", TextType.CODE)
        new_list2 = split_nodes_delimiter(new_list, "_", TextType.ITALIC)
        new_list3 = split_nodes_delimiter(new_list2, "**", TextType.BOLD)
        self.assertEqual(new_list3, [TextNode("This is some ", "text", None), TextNode("code block", "code", None), TextNode(" blabla. Here is some ", "text", None), TextNode("bold text", "bold", None), TextNode(" followed by ", "text", None), TextNode("italic text", "italic", None), TextNode(" and nothing else!", "text", None)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        
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
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
            )
        
    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
            )
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
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
        ],
        result,
        )
        
if __name__ == "__main__":
    unittest.main()