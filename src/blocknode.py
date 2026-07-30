from enum import Enum

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_leaf_node


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING1 = "Heading 1"
    HEADING2 = "Heading 2"
    HEADING3 = "Heading 3"
    HEADING4 = "Heading 4"
    HEADING5 = "Heading 5"
    HEADING6 = "Heading 6"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered list"
    ORDERED_LIST = "Ordered list"


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("# "):
        return BlockType.HEADING1

    elif block.startswith("## "):
        return BlockType.HEADING2

    elif block.startswith("### "):
        return BlockType.HEADING3

    elif block.startswith("#### "):
        return BlockType.HEADING4

    elif block.startswith("##### "):
        return BlockType.HEADING5

    elif block.startswith("###### "):
        return BlockType.HEADING6

    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    elif block.startswith(">"):
        is_quote = True
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    elif block.startswith("- "):
        is_unordered_list = True
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST

    elif block.startswith("1. "):
        is_ordered_list = True
        lines = block.split("\n")
        for i in range(2, len(lines)):
            if not lines[i - 1].startswith(f"{i}. "):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH


def block_to_node_directly(block: str, block_type: BlockType) -> ParentNode:
    from mdextractor import text_to_textnodes

    match (block_type):
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            block = " ".join([line.strip() for line in lines])
            text_nodes = text_to_textnodes(block)
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]
            return ParentNode("p", leaf_nodes)

        case BlockType.HEADING1:
            text_nodes = text_to_textnodes(block.removeprefix("# "))
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]
            return ParentNode("h1", leaf_nodes)

        case BlockType.HEADING2:
            text_nodes = text_to_textnodes(block.removeprefix("## "))
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]
            return ParentNode("h2", leaf_nodes)

        case BlockType.HEADING3:
            text_nodes = text_to_textnodes(block.removeprefix("### "))
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]
            return ParentNode("h3", leaf_nodes)

        case BlockType.HEADING4:
            text_nodes = text_to_textnodes(block.removeprefix("#### "))
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]
            return ParentNode("h4", leaf_nodes)

        case BlockType.HEADING5:
            text_nodes = text_to_textnodes(block.removeprefix("##### "))
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]
            return ParentNode("h5", leaf_nodes)

        case BlockType.HEADING6:
            text_nodes = text_to_textnodes(block.removeprefix("###### "))
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]
            return ParentNode("h6", leaf_nodes)

        case BlockType.CODE:
            text_node = TextNode(
                block.removeprefix("```\n").removesuffix("```"), TextType.PLAIN_TEXT
            )
            leaf_node = text_node_to_leaf_node(text_node)
            return ParentNode("pre", [ParentNode("code", [leaf_node])])

        case BlockType.QUOTE:
            lines = block.split("\n")
            # lines_text_nodes: list[list[TextNode]] = [
            #     text_to_textnodes(line.removeprefix(">")) for line in lines
            # ]

            # lines_leaf_nodes: list[list[LeafNode]] = []
            # for line_text_nodes in lines_text_nodes:
            #     lines_leaf_nodes.append(
            #         [text_node_to_leaf_node(text_node) for text_node in line_text_nodes]
            #     )

            # parent_p_nodes: list[ParentNode] = [
            #     ParentNode("p", line_leaf_nodes) for line_leaf_nodes in lines_leaf_nodes
            # ]

            lines_without_prefix = [line.removeprefix(">") for line in lines]
            block = " ".join([line.strip() for line in lines_without_prefix])
            text_nodes = text_to_textnodes(block)
            leaf_nodes = [text_node_to_leaf_node(text_node) for text_node in text_nodes]

            return ParentNode("blockquote", leaf_nodes)

        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            lines_text_nodes = [
                text_to_textnodes(line.removeprefix("- ")) for line in lines
            ]

            lines_leaf_nodes: list[list[LeafNode]] = []
            for line_text_nodes in lines_text_nodes:
                lines_leaf_nodes.append(
                    [text_node_to_leaf_node(node) for node in line_text_nodes]
                )

            parent_li_nodes = [
                ParentNode("li", line_leaf_nodes)
                for line_leaf_nodes in lines_leaf_nodes
            ]

            return ParentNode("ul", parent_li_nodes)

        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            lines_text_nodes = [text_to_textnodes(line[3:]) for line in lines]

            lines_leaf_nodes: list[list[LeafNode]] = []
            for line_text_nodes in lines_text_nodes:
                lines_leaf_nodes.append(
                    [text_node_to_leaf_node(node) for node in line_text_nodes]
                )

            parent_li_nodes = [
                ParentNode("li", line_leaf_nodes)
                for line_leaf_nodes in lines_leaf_nodes
            ]

            return ParentNode("ol", parent_li_nodes)
