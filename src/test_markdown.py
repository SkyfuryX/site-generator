import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import (
    text_to_html, 
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_blocktype,
    BlockType,
    markdown_to_html_node
)


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
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,)
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_blocktype(self):
        md = """
>quote
>quote
>quote
>quote
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_blocktype(blocks[0]),BlockType.QUOTE)
        
        md = """This is a paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_blocktype(blocks[0]),BlockType.PARAGRAPH)
        
        md = """## This is a paragraph as a header"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_blocktype(blocks[0]),BlockType.HEADING)
        
        md = """- list\n- list\n- list"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_blocktype(blocks[0]),BlockType.UO_LIST)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_lists(self):
        md = '''
- this is a list
- this is a list with **bold** in it
- this list also has _italic_        
'''
        node = markdown_to_html_node(md) # Unordered list
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>this is a list</li><li>this is a list with <b>bold</b> in it</li><li>this list also has <i>italic</i></li></ul></div>")
        
        md = """
1. first
2. second
3. third
"""

        node = markdown_to_html_node(md) # Ordered list
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_quotes(self):
        md = '''
>this is a quote.
>this is a quote with **bold** in it.
>this quote also has _italic_.
'''
        node = markdown_to_html_node(md) # Unordered list
        html = node.to_html()
        self.assertEqual(html, "<div><quoteblock>this is a quote. this is a quote with <b>bold</b> in it. this quote also has <i>italic</i>.</quoteblock></div>")
        

if __name__ == "__main__":
    unittest.main()