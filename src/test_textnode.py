import unittest
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    split_nodes_delimiter,
)


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://wikipedia.org"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.PLAIN),
            ],
            new_nodes,
        )


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
