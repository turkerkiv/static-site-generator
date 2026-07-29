from test_markdown import md
from mdextractor import markdown_to_html_root_node


def main():
    parent_node = markdown_to_html_root_node(md)
    print(parent_node.to_html())


if __name__ == "__main__":
    main()
