from src.block_transformer import markdown_to_block, block_to_BlockType, BlockType
import unittest


class TestMarkdownBlockToBlock(unittest.TestCase):
    def test_markdown_to_block_regular(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
    
        blocks = markdown_to_block(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
            )



    def test_markdown_to_blocks_many_unnecessary_newlines(self):
        md = """
\n\n\nThis is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items\n
    """
        blocks = markdown_to_block(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
        )



    def test_markdown_to_blocks_empty(self):
        md = """"""
        blocks = markdown_to_block(md)
        self.assertEqual(blocks, [],)


    def test_markdown_to_blocks_it_is_stripped(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line\n\n useless hello

- This is a list
- With items
    """
        blocks = markdown_to_block(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "useless hello", #the spaces get stripped
            "- This is a list\n- With items"
        ],
        )






class TestBlockType(unittest.TestCase):

    def test_block_type_heading(self):
        md =  "### hello"
        expected_block_type = BlockType.HEADING
        actual_block_type = block_to_BlockType(md)
        self.assertEqual(actual_block_type, expected_block_type)

    def test_block_type_fake_heading(self):
        md =  "###hello"
        expected_block_type = BlockType.PARAGRAPH
        actual_block_type = block_to_BlockType(md)
        self.assertEqual(actual_block_type, expected_block_type)

    def test_block_type_code(self):
        md =  """```from my_life import happiness
ImportError: cannot import name 'not_exist' from 'actual_real'
```"""
        expected_block_type = BlockType.CODE
        actual_block_type = block_to_BlockType(md)
        self.assertEqual(actual_block_type, expected_block_type)

    def test_block_type_unordered_list(self):
        md =  """
- sheep 1
- sheep 2
- sheep 3
"""
        expected_block_type = BlockType.UNORDERED_LIST
        actual_block_type = block_to_BlockType(md)
        self.assertEqual(actual_block_type, expected_block_type)

    def test_block_type_ordered_list(self):
        md =  """
1. sheep 1
2. sheep 2
3. sheep 3
"""
        expected_block_type = BlockType.ORDERED_LIST
        actual_block_type = block_to_BlockType(md)
        self.assertEqual(actual_block_type, expected_block_type)

    def test_block_type_quote(self):
        md =  """
> "You never gonna lose if you dont try"
> "But someone who fails is infinitely closer to winning than those who never try
"""
        expected_block_type = BlockType.QUOTE
        actual_block_type = block_to_BlockType(md)
        self.assertEqual(actual_block_type, expected_block_type)