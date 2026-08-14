import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_default_value(self):
        # Test is regular value work
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_none(self):
        # Test is props_to_html fuction correctly
        node = HTMLNode(tag="a", value="Test")
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises_not_implemented(self):
        # Test is error raise correct
        node = HTMLNode(tag="p", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        # Test string repr(representation) correct
        node = HTMLNode(tag="p", value="Hello World")
        expected = "HTMLNode(p, Hello World, None, None)"
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Dry Hello, world!")
        self.assertEqual(node.to_html(), "Dry Hello, world!")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "totally not rickroll", {"href": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        self.assertEqual(node.to_html(), '<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">totally not rickroll</a>')

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

    def test_to_html_with_grandgrandchildren(self):
        grandgrandchild_node = LeafNode("b", "grandgrandchild")
        grandchild_node = ParentNode("p", [grandgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>grandgrandchild</b></p></span></div>",
        )

    def test_to_html_with_grandgrandchild_that_have_link(self):
        grandgrandchild_node = LeafNode("b", "grandgrandchild", {"href": "https://sigma"})
        grandchild_node = ParentNode("p", [grandgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><p><b href="https://sigma">grandgrandchild</b></p></span></div>',
        )

    def test_to_html_with_parent_that_have_link(self):
        grandgrandchild_node = LeafNode("b", "grandgrandchild", {"href": "https://sigma"})
        grandchild_node = ParentNode("p", [grandgrandchild_node])
        child_node = ParentNode("span", [grandchild_node], {"href": "https://mari"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span href="https://mari"><p><b href="https://sigma">grandgrandchild</b></p></span></div>',
        )



if __name__ == "__main__":
    unittest.main()