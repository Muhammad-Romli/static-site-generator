import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Yo Mama", TextType.BOLD)
        node2 = TextNode("Respect your Mom", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("I Love Devil Spire Falls", TextType.BOLD)
        node2 = TextNode("I Love Devil Spire Falls", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("I Love Devil Spire Falls", TextType.BOLD, "https://matias.me/nsfw/") #this is just ditto dancing
        node2 = TextNode("I Love Devil Spire Falls", TextType.TEXT, "https://aidn.jp/wowa/") #this is miku dancing
        self.assertNotEqual(node, node2)       

class TestTextTypeNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://i")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://i", "alt": "This is a image node"})

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://love")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://love"})


if __name__ == "__main__":
    unittest.main()
