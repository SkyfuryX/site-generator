from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode

class TextType(Enum):
    TEXT = "text" # text (plain)
    BOLD = "bold" # **Bold text**
    ITALIC = "italic" # _Italic text_
    CODE = "code" # `Code text`
    LINK = "link" # Links, in this format: [anchor text](url)
    IMAGE = "image" # Images, in this format: ![alt text](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text # text of the node
        self.text_type = text_type # type of text (TextType Enum)
        self.url = url # URL of link or image
        
    def __eq__(self, node):
        if all((self.text == node.text
                ,self.text_type == node.text_type
                ,self.url == node.url)):
            return True
        return False    
        
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    
def text_to_html(text_node):
    if text_node.text_type not in TextType:
        raise Exception("NOt a valid TextType")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", '', {"src": text_node.url, "alt":text_node.text} )