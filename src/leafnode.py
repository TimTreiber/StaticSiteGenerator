from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, children = None, props = props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNodes must have a value.")
        elif self.tag == None:
            return self.value
        else:
            string = "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"
            return string