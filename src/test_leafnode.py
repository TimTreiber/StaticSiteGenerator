import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "some text", {"href": "https://www.google.com"})
        node3 = LeafNode("p", "some text", {"href": "https://www.google.com", "target": "_blank"})
        
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<p href="https://www.google.com">some text</p>')
        self.assertEqual(node3.to_html(), '<p href="https://www.google.com" target="_blank">some text</p>')

        


if __name__ == "__main__":
    unittest.main()