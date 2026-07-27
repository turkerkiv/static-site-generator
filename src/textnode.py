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


# at first made without using split but being multiple charactered delimiter was not supported. So I made it with split.
def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result_nodes = []
    for node in old_nodes:
        # we only split text nodes. no nested allowed
        if node.text_type != TextType.PLAIN_TEXT:
            result_nodes.append(node)
            continue

        # even parts means there is odd number of delimiters which is invalid markdown syntax
        parts = node.text.split(delimiter)
        if len(parts) % 2 != 1:
            raise Exception("Invalid markdown syntax")

        for i in range(len(parts)):
            # it handles the case where there are starting with delimiter and ending with delimiter and also the case where there are multiple delimiters in a row as there will be "" empty strings in the parts list
            if i % 2 == 0 and parts[i] != "":
                result_nodes.append(TextNode(parts[i], TextType.PLAIN_TEXT))
            elif i % 2 == 1:
                result_nodes.append(TextNode(parts[i], text_type))

    return result_nodes
