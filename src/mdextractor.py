from blocknode import BlockType, block_to_block_type, block_to_node_directly
from parentnode import ParentNode
from textnode import TextNode, TextType
import re


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result_nodes = []
    for node in old_nodes:
        # we only split text nodes. no nested allowed
        if node.text_type != TextType.PLAIN_TEXT:
            result_nodes.append(node)
            continue

        matches_tuples = extract_markdown_images(node.text)
        if len(matches_tuples) == 0:
            result_nodes.append(TextNode(node.text, TextType.PLAIN_TEXT))
            continue

        text_parts = []
        remaining_part = node.text
        for i in range(len(matches_tuples)):
            text_parts = remaining_part.split(
                f"![{matches_tuples[i][0]}]({matches_tuples[i][1]})"
            )

            remaining_part = text_parts[1]
            if text_parts[0] != "":
                result_nodes.append(TextNode(text_parts[0], TextType.PLAIN_TEXT))

            result_nodes.append(
                TextNode(matches_tuples[i][0], TextType.IMAGE, matches_tuples[i][1])
            )

        if remaining_part != "":
            result_nodes.append(TextNode(remaining_part, TextType.PLAIN_TEXT))

    return result_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result_nodes = []
    for node in old_nodes:
        # we only split text nodes. no nested allowed
        if node.text_type != TextType.PLAIN_TEXT:
            result_nodes.append(node)
            continue

        matches_tuples = extract_markdown_links(node.text)
        if len(matches_tuples) == 0:
            result_nodes.append(TextNode(node.text, TextType.PLAIN_TEXT))
            continue

        text_parts = []
        remaining_part = node.text
        for i in range(len(matches_tuples)):
            text_parts = remaining_part.split(
                f"[{matches_tuples[i][0]}]({matches_tuples[i][1]})"
            )

            remaining_part = text_parts[1]
            if text_parts[0] != "":
                result_nodes.append(TextNode(text_parts[0], TextType.PLAIN_TEXT))

            result_nodes.append(
                TextNode(matches_tuples[i][0], TextType.LINK, matches_tuples[i][1])
            )

        if remaining_part != "":
            result_nodes.append(TextNode(remaining_part, TextType.PLAIN_TEXT))

    return result_nodes


def extract_markdown_images(text: str) -> list[str]:
    # matches = re.findall(r"!\[(.*?)\]\((https:\/\/.*?\..*?)\)", text) - it was mine
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[str]:
    # matches = re.findall(r"(?<!\!)\[(.*?)\]\((https:\/\/.*?\..*?)\)", text) - it was mine
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def text_to_textnodes(text: str) -> list[TextNode]:
    result_nodes = split_nodes_delimiter(
        [TextNode(text, TextType.PLAIN_TEXT)], "**", TextType.BOLD_TEXT
    )
    result_nodes = split_nodes_delimiter(result_nodes, "_", TextType.ITALIC_TEXT)
    result_nodes = split_nodes_delimiter(result_nodes, "`", TextType.CODE_TEXT)
    result_nodes = split_nodes_image(result_nodes)
    result_nodes = split_nodes_link(result_nodes)
    return result_nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    # takes whole markdown file and seperates it into blocks
    # assuming markdown has newline between blocks as it is properly formatted markdown
    blocks = markdown.split("\n\n")
    checked_blocks = []
    for block in blocks:
        if block.strip() != "":
            checked_blocks.append(block.strip())
    return checked_blocks


def whole_markdown_to_html_node(markdown: str) -> ParentNode:
    # converts whole markdown file to html node tree
    blocks = markdown_to_blocks(markdown)
    parent_html_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_node_directly(block, block_type)
        parent_html_node.children.append(node)

    return parent_html_node


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.removeprefix("# ")
    raise Exception("No h1 in markdown")
