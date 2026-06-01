import os
import shutil

from markdown_blocks import markdown_to_html_node


def copy_src_dest(src="static", dest="public", top_level=False):
    if top_level and os.path.exists(dest) and os.path.isdir(dest):
        print(f"removing directory: {dest}")
        shutil.rmtree(dest)

    if not os.path.exists(dest):
        print(f"creating directory: {dest}")
        os.mkdir(dest)

    items = os.listdir(src)
    for list_item in items:
        full_path = os.path.join(src, list_item)
        if os.path.isfile(full_path):
            print(f"copying file: {full_path} - from {src} to {dest}")
            shutil.copy(full_path, dest)
        elif os.path.isdir(full_path):
            print(f"found directory: {full_path}")
            copy_src_dest(full_path, os.path.join(dest, list_item))
        print("done...\n")


def extract_title(markdown: str):
    for line in markdown.splitlines():
        if line.strip().startswith("# "):
            title = line[1:].strip()
            return title
    raise ValueError("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        print(f"Reading {from_path}")
        with open(from_path, "r") as f:
            markdown = f.read()

        print(f"Reading {template_path}")
        with open(template_path, "r") as f:
            template = f.read()

        print("Converting markdown to html")
        html_str = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html_str)

        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            print(f"Creating directory: {dest_dir}")
            os.makedirs(dest_dir)

        print(f"Writing {dest_path}")
        with open(dest_path, "w") as f:
            f.write(template)

    except OSError as oe:
        print(f"OS Error: {oe}")
        raise oe
    except Exception as e:
        print(f"Error: {e}")
        raise e



