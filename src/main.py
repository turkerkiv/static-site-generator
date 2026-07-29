from test_markdown import md
from mdextractor import markdown_to_html_root_node
import os
import shutil

project_path = os.path.abspath(".")
public_dir_path = os.path.join(project_path, "public")
static_dir_path = os.path.join(project_path, "static")


def main():
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
    os.mkdir(public_dir_path)
    copy_files_to_public(static_dir_path, public_dir_path)


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


if __name__ == "__main__":
    main()
