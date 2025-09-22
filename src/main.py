from textnode import TextNode
from textnode import TextType
from leafnode import LeafNode

def main():
    newNode = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(newNode)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGES:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid Enum type.")

if __name__ == "__main__":
    main()
