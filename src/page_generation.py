import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# ") and len(line) > 2:
            return line[2:]

    raise Exception("No h1 header provided in the markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        contents = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(contents).to_html()
    title = extract_title(contents)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as file:
        file.write(template)
