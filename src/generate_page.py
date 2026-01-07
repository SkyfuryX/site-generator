from inline_markdown import (markdown_to_html_node,
                              markdown_to_blocks)
import os, logging

logging.basicConfig(level=logging.INFO)

def open_file(location):
    with open(location, "r") as file:
        return file.read()
    
def write_file(location, content):
    with open(location, "w") as file:
        file.write(content)

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block.startswith("# "):
            return block.lstrip("# ")
        
def generate_page(from_path, template_path, dest_path):
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open_file(from_path)
    template = open_file(template_path)
    node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", node.to_html())
    write_file(dest_path, template)