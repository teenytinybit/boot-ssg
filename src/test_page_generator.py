import unittest

from page_generator import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# This is a title")
        self.assertEqual(title, "This is a title")

    def test_extract_title_no_markdown(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_extract_title_no_hash(self):
        with self.assertRaises(ValueError):
            extract_title("This is not a title")

    def test_extract_title_empty_string(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_extract_title_invalid_level(self):
        with self.assertRaises(ValueError):
            extract_title("## This is not a title")

        with self.assertRaises(ValueError):
            extract_title("### This is not a title")

        with self.assertRaises(ValueError):
            extract_title("#### This is not a title")

    def test_extract_title_no_space(self):
        with self.assertRaises(ValueError):
            extract_title("#This is not a title")


if __name__ == "__main__":
    unittest.main()
