import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node.url, "https://google.com")


class TestMisc(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props["href"], "https://google.com")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://google.com")

    def test_image_with_alt(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://google.com")
        self.assertEqual(html_node.props["alt"], "This is a text node")


# bold, italics, code ticks
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        nodes = split_nodes_delimiter(
            [TextNode("hello world **how are you**? **fine**!!!", TextType.PLAIN)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("hello world ", TextType.PLAIN),
                TextNode("how are you", TextType.BOLD),
                TextNode("? ", TextType.PLAIN),
                TextNode("fine", TextType.BOLD),
                TextNode("!!!", TextType.PLAIN),
            ],
        )

    def test_split_nodes_delimiter_italics(self):
        nodes = split_nodes_delimiter(
            [TextNode("hello world _how are you_? _fine_!!!", TextType.PLAIN)],
            "_",
            TextType.ITALIC,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("hello world ", TextType.PLAIN),
                TextNode("how are you", TextType.ITALIC),
                TextNode("? ", TextType.PLAIN),
                TextNode("fine", TextType.ITALIC),
                TextNode("!!!", TextType.PLAIN),
            ],
        )

    def test_split_nodes_delimiter_code(self):
        nodes = split_nodes_delimiter(
            [TextNode("hello world `how are you`? `fine`!!!", TextType.PLAIN)],
            "`",
            TextType.CODE,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("hello world ", TextType.PLAIN),
                TextNode("how are you", TextType.CODE),
                TextNode("? ", TextType.PLAIN),
                TextNode("fine", TextType.CODE),
                TextNode("!!!", TextType.PLAIN),
            ],
        )

    def test_multiple_nodes(self):
        nodes = split_nodes_delimiter(
            [
                TextNode("hello world **how are you**? **fine**!!!", TextType.PLAIN),
                TextNode("hello world _how are you_? _fine_!!!", TextType.PLAIN),
                TextNode("hello world `how are you`? `fine`!!!", TextType.PLAIN),
            ],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            nodes,
            [
                TextNode("hello world ", TextType.PLAIN),
                TextNode("how are you", TextType.BOLD),
                TextNode("? ", TextType.PLAIN),
                TextNode("fine", TextType.BOLD),
                TextNode("!!!", TextType.PLAIN),
                TextNode("hello world _how are you_? _fine_!!!", TextType.PLAIN),
                TextNode("hello world `how are you`? `fine`!!!", TextType.PLAIN),
            ],
        )

    def test_delimiter_at_start_pos(self):
        nodes = split_nodes_delimiter(
            [TextNode("**how are you** hey", TextType.PLAIN)],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            nodes,
            [TextNode("how are you", TextType.BOLD), TextNode(" hey", TextType.PLAIN)],
        )

    def test_delimiter_at_end_pos(self):
        nodes = split_nodes_delimiter(
            [TextNode("hey, _how are you_", TextType.PLAIN)],
            "_",
            TextType.ITALIC,
        )

        self.assertEqual(
            nodes,
            [
                TextNode("hey, ", TextType.PLAIN),
                TextNode("how are you", TextType.ITALIC),
            ],
        )

    def test_delimiter_not_balanced(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [TextNode("**how are you** today **?", TextType.PLAIN)],
                "**",
                TextType.BOLD,
            )

    def test_multiple_different_delimiters(self):
        nodes = split_nodes_delimiter(
            [TextNode("hello world `how are you`? **fine**!!!", TextType.PLAIN)],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            nodes,
            [
                TextNode("hello world ", TextType.PLAIN),
                TextNode("how are you", TextType.CODE),
                TextNode("? **fine**!!!", TextType.PLAIN),
            ],
        )

    def test_no_delimiter(self):
        nodes = split_nodes_delimiter(
            [TextNode("hello world", TextType.PLAIN)],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            nodes,
            [TextNode("hello world", TextType.PLAIN)],
        )

    def test_empty_string(self):
        nodes = split_nodes_delimiter(
            [TextNode("", TextType.PLAIN)],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            nodes,
            [TextNode("", TextType.PLAIN)],
        )

    def test_non_text_node(self):
        nodes = split_nodes_delimiter(
            [TextNode("**hello world**", TextType.BOLD)],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            nodes,
            [TextNode("**hello world**", TextType.BOLD)],
        )

    def test_empty_nodes(self):
        nodes = split_nodes_delimiter([], "**", TextType.BOLD)

        self.assertEqual(nodes, [])

    def test_delimiter_entire_string(self):
        nodes = split_nodes_delimiter(
            [TextNode("**how are you**", TextType.PLAIN)],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            nodes,
            [TextNode("how are you", TextType.BOLD)],
        )


if __name__ == "__main__":
    unittest.main()
