import unittest

from mdextractor import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_split_nodes_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is text with no delimiter", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_multiple_delimiters(self):
        node = TextNode(
            "This is text with multiple `code block` words `in it`", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with multiple ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(new_nodes[2].text, " words ")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "in it")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE_TEXT)

    def test_split_nodes_bold_delimiter(self):
        node = TextNode(
            "This is text with multiple **bold** words **in it**", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with multiple ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[2].text, " words ")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "in it")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_non_text_node(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a bold text node")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_multiple_old_nodes(self):
        node1 = TextNode("This is a **bold1** text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a **bold2** text node", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "bold1")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[2].text, " text node")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "This is a ")
        self.assertEqual(new_nodes[3].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[4].text, "bold2")
        self.assertEqual(new_nodes[4].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[5].text, " text node")
        self.assertEqual(new_nodes[5].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_no_match_delimiters(self):
        node = TextNode(
            "This is text with no `matching delimiters", TextType.PLAIN_TEXT
        )
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](https://example.com/1.png) and ![two](https://example.com/2.png)"
        )
        self.assertListEqual(
            [
                ("one", "https://example.com/1.png"),
                ("two", "https://example.com/2.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_false_ones(self):
        matches = extract_markdown_images(
            "Not an image: [image](https://example.com/1.png) and ![broken](missing"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[one](https://example.com/1) and [two](https://example.com/2)"
        )
        print(matches)
        self.assertListEqual(
            [("one", "https://example.com/1"), ("two", "https://example.com/2")],
            matches,
        )

    def test_extract_markdown_links_false_ones(self):
        matches = extract_markdown_links(
            "Not a link: (https://example.com) and [broken](missing"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_tricky_mixed_text(self):
        text = (
            "Start ![img](https://example.com/img.png) mid [link](https://example.com) "
            "end ![alt text](https://example.com/a-b_c.png) and [another](https://example.com?q=1)"
        )
        self.assertListEqual(
            [
                ("img", "https://example.com/img.png"),
                ("alt text", "https://example.com/a-b_c.png"),
            ],
            extract_markdown_images(text),
        )
        self.assertListEqual(
            [
                ("link", "https://example.com"),
                ("another", "https://example.com?q=1"),
            ],
            extract_markdown_links(text),
        )


if __name__ == "__main__":
    unittest.main()
