from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    PLAIN_TEXT = "Plain"
    BOLD_TEXT = "Bold"
    ITALIC_TEXT = "Italic"
    CODE_TEXT = "Code"
    LINK = "Link"
    IMAGE = "Image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown TextNode Type")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    # did not wanna use split() as i wanted to implement it myself
    result_nodes = []
    for node in old_nodes:
        # we only split text nodes. no nested allowed
        if node.text_type != TextType.PLAIN_TEXT:
            result_nodes.append(node)
            continue

        # it converts one textnode with combined texttypes into multiple seperated textnodes
        delimiter_count = node.text.count(delimiter)
        delimiters = [delimiter for i in range(delimiter_count)]
        if delimiter_count % 2 != 0:
            raise Exception(
                "Matching closing delimiter not found, invalid markdown syntax"
            )

        text = ""
        for c in node.text:
            if c == delimiter:
                delimiters.pop()
                # it is end of text that is before the delimiter
                if len(delimiters) % 2 != 0:
                    result_nodes.append(TextNode(text, TextType.PLAIN_TEXT))
                # it is end of text that is inside delimiter
                else:
                    result_nodes.append(TextNode(text, text_type))
                text = ""
                continue

            text += c

        # if there is text after the delimiter
        if not text == "":
            result_nodes.append(TextNode(text, TextType.PLAIN_TEXT))

    return result_nodes
