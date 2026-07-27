import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("div", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node = ParentNode("div", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("h1", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<h1><div><div>grandchild1</div><p>grandchild2</p></div></h1>",
        )

    def test_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("div", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2")
        grandchild_node3 = LeafNode("h2", "grandchild3")
        child_node1 = ParentNode("div", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("div", [grandchild_node3])
        parent_node = ParentNode("h1", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<h1><div><div>grandchild1</div><p>grandchild2</p></div><div><h2>grandchild3</h2></div></h1>",
        )

    def test_to_html_with_empty_child_list(self):
        parent_node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_child(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()
