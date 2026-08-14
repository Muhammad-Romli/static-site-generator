from src.file_operator.set_up_html import extract_title
import unittest

class TestExtractTitle(unittest.TestCase):
    def test_regular_extract_title(self):
        markdown = """
# This is the title
## This is the subtitle

Hello  world, lorem ipsum dolor sit amet
Hello  world, lorem ipsum dolor sit amet
"""
        actual_result = extract_title(markdown)
        expected_result = "This is the title"
        self.assertEqual(actual_result, expected_result)

    def test_fake_double_extract_title(self):
        markdown = """
# This is the title
# Double title that shouldnt be count

Hello  world, lorem ipsum dolor sit amet
Hello  world, lorem ipsum dolor sit amet
"""
        actual_result = extract_title(markdown)
        expected_result = "This is the title"
        self.assertEqual(actual_result, expected_result)

    def test_no_title_extract_title(self):
        markdown = """
Hello  world, lorem ipsum dolor sit amet
Hello  world, lorem ipsum dolor sit amet
"""
        self.assertRaisesRegex(Exception, 
                               r'make sure to put line with single \"#\"\(h1\) inside of your markdown',
                               extract_title, 
                               markdown
                               )


