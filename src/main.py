import os

from utilites import copy_directory
from page_generation import generate_pages_recursive


def main():
    static_path = os.path.join(os.getcwd(), "static")
    public_path = os.path.join(os.getcwd(), "public")
    copy_directory(static_path, public_path)

    content_path = os.path.join(os.getcwd(), "content")
    template_path = os.path.join(os.getcwd(), "template.html")
    destination_path = os.path.join(os.getcwd(), "public")
    generate_pages_recursive(content_path, template_path, destination_path)

main()
