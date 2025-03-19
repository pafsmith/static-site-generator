from copy_public import copy_directory
from textnode import TextNode, TextType
from blocktype import markdown_to_html_node
import re
import os
import shutil
from pathlib import Path
import sys


def extract_title(markdown_content):
    """Extract title from markdown content."""
    match = re.match(r"^#\s+(.*)$", markdown_content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Untitled"

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    """
    Recursively generate HTML pages from markdown files in a directory.
    
    Args:
        dir_path_content: Source directory containing markdown files
        template_path: Path to the template HTML file
        dest_dir_path: Destination directory for generated HTML files
        base_path: Base URL path for the site
    """
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(source_path):
            if source_path.endswith('.md'):
                rel_path = os.path.relpath(source_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, Path(rel_path).stem + '.html')
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(source_path, template_path, dest_path, base_path)
        
        elif os.path.isdir(source_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(source_path, template_path, new_dest_dir, base_path)

def generate_page(markdown_path, template_path, output_path, base_path):
    """Generate an HTML page from markdown content and template."""
    print(f"Generating Page from {markdown_path} to {output_path} using {template_path}")
    
    with open(markdown_path, "r") as f:
        markdown_content = f.read()
    
    title = extract_title(markdown_content)
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    with open(template_path, "r") as f:
        template = f.read()
    
    # Replace content placeholders
    output_html = template.replace("{{ Title }}", title)
    output_html = output_html.replace("{{ Content }}", html_content)
    
    # Replace base path in URLs
    output_html = output_html.replace('href="/', f'href="{base_path}')
    output_html = output_html.replace('src="/', f'src="{base_path}')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(output_html)


def main():
    """Main function to generate the static site."""
    # Get base path from command line argument or use default
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/docs"
    
    # Set up paths
    content_dir = "./content"
    template_path = "./template.html"
    output_dir = "./docs"  # Changed from public to docs
    
    # Clean and recreate output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # Copy static files
    if os.path.exists("./static"):
        for item in os.listdir("./static"):
            source = os.path.join("./static", item)
            dest = os.path.join(output_dir, item)
            if os.path.isfile(source):
                print(f"Copying file: {source} to {dest}")
                shutil.copy2(source, dest)
            elif os.path.isdir(source):
                print(f"Copying directory: {source} to {dest}")
                shutil.copytree(source, dest)
    
    # Generate HTML pages from markdown files
    generate_pages_recursive(content_dir, template_path, output_dir, base_path)


if __name__ == "__main__":
    main()
