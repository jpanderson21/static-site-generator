class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ""
        if self.props is not None:
            for key, value in self.props.items():
                html += f' {key}="{value}"'
        return html

    def __repr__(self):
        return f"HTMLNode:\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes require a value.")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes require a tag.")
        elif self.children is None:
            raise ValueError("Parent nodes require children.")

        html = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            html += node.to_html()
        html += f"</{self.tag}>"

        return html
