import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        test_node = HTMLNode("p", "some text", [], {"href": "https://www.google.com"})
        node = HTMLNode("p", "some text", props = {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "some text", props = {"href": "https://www.google.com"})
        node3 = HTMLNode("p", "some text", [], {"href": "https://www.google.com"})
        node4 = HTMLNode("p", "some text", [test_node], {"href": "https://www.google.com"})
        node5 = HTMLNode("p", "some text", [test_node], {"href": "https://www.google.com"})
        #print(node5.props_to_html())
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertEqual(node4, node5)
        


if __name__ == "__main__":
    unittest.main()