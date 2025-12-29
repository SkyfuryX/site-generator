import unittest

from textnode import (TextNode, TextType)
from inline_markdown import (text_to_html, 
                    split_nodes_delimiter, 
                    extract_markdown_images, 
                    extract_markdown_links, 
                    split_nodes_image, 
                    split_nodes_link,
                    text_to_textnodes)


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
        
class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")  
        
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")        
        
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")
                
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")
        
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.google.com")
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="www.google.com">This is a link node</a>')
        
    def test_image(self):
        node = TextNode("google holiday image", TextType.IMAGE, "https://www.google.com/logos/doodles/2025/seasonal-holidays-2025-6753651837110711.4-la1f1f1f.gif")
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="https://www.google.com/logos/doodles/2025/seasonal-holidays-2025-6753651837110711.4-la1f1f1f.gif" alt="google holiday image"></img>')

class TestDeliminator(unittest.TestCase):
    def testText(self):
        pass
    
    def testCode(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
    
    def testBold(self):
        node = TextNode("This is **very** cool **indeed**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("very", TextType.BOLD),
            TextNode(" cool ", TextType.TEXT),
            TextNode("indeed", TextType.BOLD),
            ])        

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        matches = extract_markdown_images(
            "This is text with an ![Google holiday banner](https://www.google.com/logos/doodles/2025/stranger-things-6753651837111204-la1f1f1f.gif)"
        )
        self.assertListEqual([("Google holiday banner", "https://www.google.com/logos/doodles/2025/stranger-things-6753651837111204-la1f1f1f.gif")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This a link to [Google](https://www.google.com)"
        )
        self.assertListEqual([("Google","https://www.google.com")], matches)
        
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        print(nodes)
        # self.assertListEqual(
        #     [
        #         TextNode("This is ", TextType.TEXT),
        #         TextNode("text", TextType.BOLD),
        #         TextNode(" with an ", TextType.TEXT),
        #         TextNode("italic", TextType.ITALIC),
        #         TextNode(" word and a ", TextType.TEXT),
        #         TextNode("code block", TextType.CODE),
        #         TextNode(" and an ", TextType.TEXT),
        #         TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        #         TextNode(" and a ", TextType.TEXT),
        #         TextNode("link", TextType.LINK, "https://boot.dev"),
        #     ],
        #     nodes,)
        


if __name__ == "__main__":
    unittest.main()
