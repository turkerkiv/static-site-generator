from textnode import TextNode, TextType

def main():
    textnode = TextNode("testing text", TextType.BOLD_TEXT, "testing url")
    print(textnode)

if __name__ == "__main__":
    main()