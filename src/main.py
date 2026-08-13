from text_node import TextType, TextNode


def main():
    dummy = TextNode("this is some anchor dummy text", TextType.LINK, "https://aidn.jp/wowa/")
    print(dummy)

if __name__ == "__main__":
    main()