
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        pass

    def props_to_html(self):
        html = ""
        if not self.props == None:
            for key in self.props:
                html += f"{key}=\"{self.props[key]}\" "
            return html.rstrip()
        else:
            return ""

    def __repr__(self):
        return(f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        
        if self.props == None:
            opening_tag = f"<{self.tag}>"
        else:
            props = self.props_to_html()
            opening_tag = f"<{self.tag} {props}>"
        content = self.value
        closing_tag = f"</{self.tag}>"
        element = opening_tag + content + closing_tag

        return element

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError.add_note(self, "Missing Tag")
        if self.children == None:
            raise ValueError.add_note(self, "Missing Children")
        
        if self.props == None:
            opening_tag = f"<{self.tag}>"
        else:
            props = self.props_to_html()
            opening_tag = f"<{self.tag} {props}>"

        content = ""
        for child in self.children:
            content += child.to_html()

        closing_tag = f"</{self.tag}>"
        element = opening_tag + content + closing_tag

        return element