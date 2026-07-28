# at first made without using split but being multiple charactered delimiter was not supported. So I made it with split.
from textnode import TextNode, TextType


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
