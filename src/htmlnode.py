class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ''
        if self.props == None or self.props == {}:
            return string
        for key,value in self.props.items():
            string += f' {key}="{value}"'
        return string
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props
        
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("An HTML tag is missing")
        elif self.children is None:
            raise ValueError("Parent nodes must have children Leaf nodes")
        else:
            return f'''<{self.tag}>{''.join([child.to_html() for child in self.children])}</{self.tag}>'''
        
