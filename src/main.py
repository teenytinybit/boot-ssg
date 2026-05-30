from textnode import TextNode, TextType


def main():
    dummy = TextNode("hello", TextType.PLAIN, "https://google.com")
    print(dummy)


main()
