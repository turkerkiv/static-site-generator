import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p",
            "this node for prop to html test",
            None,
            {"className": "button-red", "id": "id1"},
        )
        self.assertEqual(node.props_to_html(), ' className="button-red" id="id1"')

    def test_repr(self):
        node = HTMLNode(
            "p",
            "this node for prop to html test",
            None,
            None,
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(Tags: p,\nValue: this node for prop to html test,\nChildren: None,\nProps: )",
        )

    def test_children_repr(self):
        child1 = HTMLNode("span", "child1", None, None)
        child2 = HTMLNode("span", "child2", None, None)
        node = HTMLNode(
            "p",
            "this node for prop to html test",
            [child1, child2],
            None,
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(Tags: p,\nValue: this node for prop to html test,\nChildren: [HTMLNode(Tags: span,\nValue: child1,\nChildren: None,\nProps: ), HTMLNode(Tags: span,\nValue: child2,\nChildren: None,\nProps: )],\nProps: )",
        )

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "this node for prop to html test", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_children_empty_list(self):
        node = HTMLNode("p", "this node for prop to html test", [], None)
        self.assertEqual(node.children, [])

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "this node for prop to html test", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
