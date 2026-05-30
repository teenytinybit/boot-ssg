import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode("div", "hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode("div", "hello", props={"class": "test"})
        self.assertEqual(node.props_to_html(), ' class="test"')

    def test_multi_props(self):
        node = HTMLNode("div", "hello", props={"class": "test", "id": "test"})
        self.assertEqual(node.props_to_html(), ' class="test" id="test"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("div", "hello", props={"class": "test"})
        self.assertEqual(node.to_html(), '<div class="test">hello</div>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!", props={"class": "test"})
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None, props={"class": "test"}).to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("div", children=[LeafNode("p", "world")])
        self.assertEqual(node.to_html(), "<div><p>world</p></div>")

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


if __name__ == "__main__":
    unittest.main()
