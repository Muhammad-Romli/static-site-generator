import unittest
from utility import split_nodes_delimiter, text_to_textnodes, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextType, TextNode


class TestSplitDelimiterCode(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected_result = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
        ]
        actual_result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(actual_result, expected_result)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        expected_result = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" word", TextType.TEXT),
        ]
        actual_result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(actual_result, expected_result)

    def test_split_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        expected_result = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word", TextType.TEXT),
        ]
        actual_result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(actual_result, expected_result)

    def test_not_exist_delimiter(self):
        node = TextNode("This is text with a ^^idk^^ word", TextType.TEXT)
        expected_result = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("^^", TextType.ITALIC),
    TextNode(" word", TextType.TEXT),
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "^^", TextType.ITALIC)

    def test_delimiter_not_in_text(self):
        node = TextNode("This is text with a ^^idk^^ word", TextType.TEXT)
        expected_result = [
    TextNode("This is text with a ^^idk^^ word", TextType.TEXT)
        ]
        self.assertEqual([node], expected_result)



class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual_result = text_to_textnodes(node)
        expected_result = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        self.assertEqual(actual_result, expected_result)

    def test_text_to_textnode_little_text(self): #is must have space, after all if it dont have space between, is invalid syntax in md file right?
        node = "**This is** **text** **with an** _italic_ _word and a_ `code block` `and an` ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual_result = text_to_textnodes(node)
        expected_result = [
    TextNode("This is", TextType.BOLD),
    TextNode(" ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" ", TextType.TEXT),
    TextNode("with an", TextType.BOLD),
    TextNode(" ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" ", TextType.TEXT),
    TextNode("word and a", TextType.ITALIC),
    TextNode(" ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" ", TextType.TEXT),
    TextNode("and an", TextType.CODE),
    TextNode(" ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        self.assertEqual(actual_result, expected_result)


    def test_text_to_textnode_bold_text_between_2_same_images(self): #is must have space, after all if it dont have space between, is invalid syntax in md file right?
        node = "![alt_text](url_text)**hello**![alt_text](url_text)"
        actual_result = text_to_textnodes(node)
        expected_result = [
            TextNode("alt_text", TextType.IMAGE, "url_text"),
            TextNode("hello", TextType.BOLD),
            TextNode("alt_text", TextType.IMAGE, "url_text")
        ]
        self.assertEqual(actual_result, expected_result)





class TestRegexFindLinks(unittest.TestCase):
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.sigma)"
        )
        self.assertListEqual([("link", "https://i.sigma")], matches)

    def test_extract_markdown_link_using_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)


    @unittest.skip("known limitation: nested parentheses in URLs not supported")
    def test_extract_markdown_link_with_double_parenthesis(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.(sig)ma)"
        )
        self.assertListEqual([], matches) #one of the condition [when it stop, it need to stop at ")"] did not meet so my regex throw it off




class TestRegexFindImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_without_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image]()"
        )
        self.assertListEqual([("image", "")], matches)

    def test_extract_markdown_images_using_link(self):
        matches = extract_markdown_images(
            "This is text with an [link](https://i.sigma)"
        )
        self.assertListEqual([], matches)

    @unittest.skip("known limitation: nested parentheses in URLs not supported")
    def test_extract_markdown_images_double_parenthesis(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.(sig)ma)"
        )
        self.assertListEqual([], matches) #one of the condition [when it stop, it need to stop at ")"] did not meet so my regex throw it off









class SplitNodesImages(unittest.TestCase):
    def test_split_2_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_only_2_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image2](https://i.imgur.com/zcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/zcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_a_whole_lot_of_nodes(self):
        node_rickroll_image = TextNode(
            "![not rickroll](https://rickroll.png)",
            TextType.TEXT,
        )
        node_text = TextNode(
            "hello",
            TextType.TEXT,
        )
        node_images = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image2](https://i.imgur.com/zcJKZ.png)",
            TextType.TEXT,
        )
        node_link = TextNode(
            "ummm [please dont see this](https://dontseethisregex)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node_rickroll_image, node_text, node_images, node_link])
        self.assertListEqual(
            [
                TextNode("not rickroll", TextType.IMAGE, "https://rickroll.png"),
                TextNode("hello", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/zcJKZ.png"),
                TextNode("ummm [please dont see this](https://dontseethisregex)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_2_same_images_with_text_only_in_between(self): #this SSG support same link
        node = TextNode(
            "![not rickroll](https://rickroll.png) this was rickroll ![not rickroll](https://rickroll.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("not rickroll", TextType.IMAGE, "https://rickroll.png"),
                TextNode(" this was rickroll ", TextType.TEXT),
                TextNode("not rickroll", TextType.IMAGE, "https://rickroll.png")
            ],
            new_nodes,
        )

    def test_split_only_2_same_images(self): #this SSG support same link
        node = TextNode(
            "![not rickroll](https://rickroll.png)![not rickroll](https://rickroll.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("not rickroll", TextType.IMAGE, "https://rickroll.png"),
                TextNode("not rickroll", TextType.IMAGE, "https://rickroll.png")
            ],
            new_nodes,
        )
    




class SplitNodesLink(unittest.TestCase):
    def test_split_2_links(self):
        node = TextNode(
            "This is text with an [link](https://rickroll) and another [second link](https://notrickrollmaybe)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://rickroll"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://notrickrollmaybe"),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://rickroll)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://rickroll")
            ],
            new_nodes,
        )

    def test_split_only_link(self):
        node = TextNode(
            "[link](https://rickroll)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://rickroll")
            ],
            new_nodes,
        )

    def test_split_only_2_same_links(self): #this SSG support same link/image
        node = TextNode(
            "[not rickroll](https://rickroll)[not rickroll](https://rickroll)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("not rickroll", TextType.LINK, "https://rickroll"),
                TextNode("not rickroll", TextType.LINK, "https://rickroll")
            ],
            new_nodes,
        )

    def test_split_2_same_links_with_text_only_in_between(self): #this support same link
        node = TextNode(
            "[not rickroll](https://rickroll) this was rickroll [not rickroll](https://rickroll)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("not rickroll", TextType.LINK, "https://rickroll"),
                TextNode(" this was rickroll ", TextType.TEXT),
                TextNode("not rickroll", TextType.LINK, "https://rickroll")
            ],
            new_nodes,
        )

    @unittest.skip("known limitation: nested parentheses in URLs not supported")
    def test_split_links_double_parenthesis(self):
        node = TextNode(
            "This is text with an [link]((https://rickroll)) and another [second link]((https://notrickrollmaybe))",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [link]((https://rickroll)) and another [second link]((https://notrickrollmaybe))", TextType.TEXT)
                #because the regex function dont find anything(because it stop at "(" instead of ")"), it spit out the node back
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()