import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()
