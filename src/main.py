from htmlnode import HTMLNode
from textnode import TextNode, TextType, split_nodes_delimiter
from leafnode import LeafNode
from parentnode import ParentNode


def main():
    textnode = TextNode("testing text", TextType.BOLD_TEXT, "testing url")
    print(textnode)
    htmlnodechild = HTMLNode("span", "This is a span", None, {"class": "my-class"})
    htmlnodechild2 = HTMLNode("span", "This is a span2", None, {"class": "my-class2"})
    htmlnode = HTMLNode(
        "p",
        "This is a paragraph",
        [htmlnodechild, htmlnodechild2],
        {"class": "my-class", "id": "my-id"},
    )
    print(htmlnode)

    leafnode1 = LeafNode("b", "hii")
    leafnode2 = LeafNode("i", "bob")
    parentnode = ParentNode("p", [leafnode1, leafnode2])
    print(parentnode.to_html())

    node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
    print(new_nodes)


if __name__ == "__main__":
    main()
