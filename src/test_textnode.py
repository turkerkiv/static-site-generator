import unittest
from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node2 which is different", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Represent test", TextType.PLAIN_TEXT, "turkerkiv.com")
        print_str = f"TextNode(Represent test,Plain,turkerkiv.com)"
        self.assertEqual(node.__repr__(), print_str)

    def test_url_none(self):
        node = TextNode("Represent test", TextType.PLAIN_TEXT)
        self.assertEqual(node.url, None)

    def test_plain_text_to_html_node(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_to_html_node(self):
        node = TextNode("This is a link node", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props_to_html(), ' href="google.com"')
        self.assertEqual(html_node.value, "This is a link node")

    def test_img_to_html_node(self):
        node = TextNode("This is an image node", TextType.IMAGE, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props_to_html(), ' src="google.com" alt="This is an image node"'
        )

    def test_bold_text_to_html_node(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_code_text_to_html_node(self):
        node = TextNode("This is a code text node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

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


if __name__ == "__main__":
    unittest.main()
