from test_markdown import md
from mdextractor import extract_title, whole_markdown_to_html_node
import os
import shutil

project_path = os.path.abspath(".")
public_dir_path = os.path.join(project_path, "public")
static_dir_path = os.path.join(project_path, "static")
content_dir_path = os.path.join(project_path, "content")


def main():
    # reset public folder
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
    os.mkdir(public_dir_path)

    copy_files_to_public(static_dir_path, public_dir_path)

    generate_page(
        os.path.join(content_dir_path, "index.md"),
        os.path.join(project_path, "template.html"),
        os.path.join(public_dir_path, "index.html"),
    )


def copy_files_to_public(from_dir_path, to_copy_path):
    for path in os.listdir(from_dir_path):
        to_be_copied_path = os.path.join(from_dir_path, path)
        print(to_be_copied_path)
        if os.path.isfile(to_be_copied_path):
            shutil.copy(to_be_copied_path, to_copy_path)
        else:
            new_folder_path = os.path.join(to_copy_path, path)
            os.mkdir(new_folder_path)
            copy_files_to_public(to_be_copied_path, new_folder_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    with open(from_path, "r") as file:
        md = file.read()

    template = ""
    with open(template_path, "r") as file:
        template = file.read()

    content_html_node = whole_markdown_to_html_node(md)
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content_html_node.to_html())

    with open(dest_path, "w") as file:
        file.write(template)


if __name__ == "__main__":
    main()
