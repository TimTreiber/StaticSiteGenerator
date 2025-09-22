import unittest

from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        node3 = TextNode("This is an image node", TextType.IMAGES, "www.gidf.com")
        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is a bold node")
        self.assertEqual(html_node3.props_to_html(), ' src="www.gidf.com" alt="This is an image node"')
        
if __name__ == "__main__":
    unittest.main()