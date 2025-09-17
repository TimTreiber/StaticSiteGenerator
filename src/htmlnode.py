class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag #html tag name (eg. p, a, h1)
        self.value = value #value of the html tag (eg. text inside of a paragraph)
        self.children = children #list of HTMLNodes
        self.props = props #dictionary representing attributes of HTML tag

    def to_html(self):
        raise NotImplementedError("missing")
    
    def props_to_html(self):
        return_string = " "
        for att in self.props:
            return_string = return_string + att + "=" + self.props[att] + " "
        return return_string
    
    def __eq__(node1, node2):
        return node1.tag == node2.tag and node1.value == node2.value and node1.children == node2.children and node1.props == node2.props

    def __repr__(self):
        return f"TextNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"