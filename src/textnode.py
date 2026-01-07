from enum import Enum

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
    

