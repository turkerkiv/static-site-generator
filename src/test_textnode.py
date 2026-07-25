import unittest
from textnode import TextNode, TextType

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
        print_str = f"TextNode(Represent test,1,turkerkiv.com)"
        self.assertEqual(node.__repr__(), print_str)
    

    def test_url_none(self):
        node = TextNode("Represent test", TextType.PLAIN_TEXT)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()