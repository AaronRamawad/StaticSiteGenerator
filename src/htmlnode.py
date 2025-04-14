
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
        if len(self.props) > 0:
            for key in self.props:
                html += f"{key}=\"{self.props[key]}\" "
        return html

    def __repr__(self):
        return(f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}")
    
