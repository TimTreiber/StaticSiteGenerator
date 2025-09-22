from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, value = None, children = children, props = props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNodes must have a value.")
        elif self.children == None:
            raise ValueError("ParentNodes must have at least one child.")
        else:
            string = "<" + self.tag + self.props_to_html() + ">"
            for child in self.children:
                string = string + child.to_html()
            string = string + "</" + self.tag + ">"
            return string