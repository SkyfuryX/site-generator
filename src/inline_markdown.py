from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from enum import Enum
import re

def text_to_html(text_node):
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
            return LeafNode("img", '', {"src": text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Not a valid TextType")
        
class BlockType(Enum):
    PARAGRAPH = "paragraph" # text (plain)
    HEADING = "heading" # #-######
    CODE = "code" # ```Code text```
    QUOTE = "quote" # >
    O_LIST = "ordered list"
    UO_LIST = "unordered list"
    
def block_to_blocktype(block):
    if block.startswith("```") and block.endswith('```'): # Code block
        return BlockType.CODE
    if block.startswith(">"): # Quote
        for line in block.split("\n"):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH 
        return BlockType.QUOTE
    if any((block.startswith("# "), #Headings
            block.startswith("## "),
            block.startswith("### "),
            block.startswith("#### "),
            block.startswith("##### "),
            block.startswith("###### "))):                     
        return BlockType.HEADING
    if block.startswith("- "): #Unordered list
        for line in block.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH 
        return BlockType.UO_LIST
    if block.startswith("1. "): #Ordered List
        for i, line in enumerate(block.split("\n")):
            if not line.startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH 
        return BlockType.O_LIST
    return BlockType.PARAGRAPH 
       
      
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split = node.text.split(delimiter)
            if delimiter not in node.text:
                new_nodes.append(node) 
                continue    
            elif len(split) % 2 == 0:
                raise Exception(f"Invalid Markdown syntax for delimiter '{delimiter}'")
            else:
                new = []
                for i, item in enumerate(split):
                    if i % 2 == 0:
                        if item != "": 
                            new.append(TextNode(item, TextType.TEXT))
                    else: 
                        new.append(TextNode(item, text_type))
                new_nodes.extend(new)
    return new_nodes
        
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        matches = extract_markdown_images(node_text)
        if not matches:
            new_nodes.append(node)
            continue
        for image_alt, image_link in matches:
            split_text = node_text.split(f"![{image_alt}]({image_link})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))    
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            node_text = split_text[1] 
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))       
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        matches = extract_markdown_links(node_text)
        if not matches:
            new_nodes.append(node)
            continue
        for text, url in matches:
            split_text = node_text.split(f"[{text}]({url})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))    
            new_nodes.append(TextNode(text, TextType.LINK, url))
            node_text = split_text[1] 
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))       
    return new_nodes

def text_to_textnodes(text):
    lines = text.split("\n")
    nodes = []
    for line in lines:
        nodes.append(TextNode(line, TextType.TEXT))
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)

def markdown_to_blocks(markdown):
    blocks = []
    split = markdown.split("\n\n")
    for item in split:
        stripped = item.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_to_html(node) for node in text_nodes]
    return html_nodes

def header_split(text):
    header = text.split(' ')
    return len(header[0]), ' '.join(header[1:])

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def ulist_to_html(block):
    sections = block.splitlines()
    return [ParentNode("li", text_to_children(section[2:])) for section in sections]

def olist_to_html(block):
    sections = block.splitlines()
    return [ParentNode("li", text_to_children(section[3:])) for section in sections]

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = [line.lstrip(">").strip() for line in lines]
    return ParentNode("blockquote", text_to_children(' '.join(new_lines))) 
    
    
def markdown_to_html_node(markdown):
    node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
       block_type = block_to_blocktype(block)
       match block_type:
           case BlockType.PARAGRAPH:
               node.children.append(paragraph_to_html_node(block))
           case BlockType.UO_LIST: 
               node.children.append(ParentNode('ul', ulist_to_html(block)))
           case BlockType.O_LIST: # FIX
               node.children.append(ParentNode('ol', olist_to_html(block)))
           case BlockType.CODE:
               code_text = block.splitlines()
               code_node = TextNode("\n".join(code_text[1:-1]) + "\n", TextType.CODE)
               node.children.append(ParentNode('pre', [text_to_html(code_node)]))
           case BlockType.HEADING:
               header = header_split(block)
               node.children.append(ParentNode(f"h{header[0]}", text_to_children(header[1])))
           case BlockType.QUOTE:
               node.children.append(quote_to_html(block))
    return node          

