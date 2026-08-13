import unittest
from markdown_transformer import markdown_to_html_node



class MarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )




    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> "What's **high tier human**"
> "To a Low Tier God"
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"What\'s <b>high tier human</b>"\n"To a Low Tier God"</blockquote></div>'
        )   


    def test_ordered_list(self):
        md = """
1. Code
2. Accidentally nap
3. Work
4. Sleep
5. Go to School
6. Nap
7. Repeat
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Code</li><li>Accidentally nap</li><li>Work</li><li>Sleep</li><li>Go to School</li><li>Nap</li><li>Repeat</li></ol></div>"
        )   