from htmlnode import HTMLNode, LeafNode
import unittest

class TestHTML(unittest.TestCase):
    def test_eq(self):
        html1 = HTMLNode("a")
        html2 = HTMLNode("a", 5, None, {
        "href": "https://www.google.com",
        "target": "_blank",
        })
        html3 = HTMLNode(None, None, html1, {})
        self.assertEqual(' href="https://www.google.com" target="_blank"', html2.props_to_html())
        self.assertEqual('', html1.props_to_html() )
        self.assertIsInstance(html3.children, HTMLNode,)  
    
class TestLeaf(unittest.TestCase):
    def testeq(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print(node1)
        self.assertEqual(node1.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node2.to_html(),"<p>This is a paragraph of text.</p>")
        node3 = LeafNode("p", "Hello, world!")
        self.assertEqual(node3.to_html(), "<p>Hello, world!</p>") 
        # node4 = LeafNode("a", None, {}) 
        # self.assert (node4.to_html(), ValueError)

if __name__ == "__main__":
    unittest.main()


# def __init__(self, tag=None, value=None, children=None, props=None):
#     self.tag = tag
#     self.value = value
#     self.children = children
#     self.props = props