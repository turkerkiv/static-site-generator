from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ):
        # dont allow children as this is leaf
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:  # it is raw text
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode(Tags: {self.tag},\nValue: {self.value},\nProps: {self.props_to_html()})"
