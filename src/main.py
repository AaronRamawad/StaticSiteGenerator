from textnode import TextNode, TextType

def main():
    example = TextNode("This is a piece of anchor text", TextType.LINK, "www.youtube.com")
    print(example)

if __name__ == "__main__":
    main()