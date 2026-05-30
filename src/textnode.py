from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    # print(delimiter)
    dl = len(delimiter)
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN or node.text == "":
            new_nodes.append(node)
            continue

        # terminate early if delimiters are not balanced
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid format")

        del_start, del_end, cursor = -dl, -dl, -dl
        while True:
            cursor = del_end + dl
            del_start = node.text.find(delimiter, cursor)
            del_end = node.text.find(delimiter, del_start + dl)
            # print(cursor, del_start, del_end)

            # if no more delimiter match
            if del_start == -1 or del_end == -1:
                text_after_del = node.text[cursor:]
                if text_after_del != "":
                    new_nodes.append(TextNode(text_after_del, TextType.PLAIN))
                    # print(text_after_del)
                break

            text_before_del = node.text[cursor:del_start]
            if text_before_del != "":
                new_nodes.append(TextNode(text_before_del, TextType.PLAIN))
                # print(text_before_del)
            new_nodes.append(
                TextNode(node.text[del_start + dl : del_end], text_type, node.url)
            )
            # print(node.text[del_start + dl : del_end])

    # print(new_nodes)
    return new_nodes
