import unittest

from textnode import TextNode, TextType


class TestNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_noteq(self):
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a link node", TextType.LINK, "www.google.com")
        self.assertNotEqual(node3, node4)
        
    def test_(self):
        node = TextNode("This is an italic node", TextType.ITALIC, None)
        node2 = TextNode("This is an italic node", TextType.ITALIC)
        self.assertEqual(node, node2)
        
        



if __name__ == "__main__":
    unittest.main()
