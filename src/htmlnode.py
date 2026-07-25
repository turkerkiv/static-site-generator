class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        str = ""
        for kv in self.props.items():
            str += f' {kv[0]}="{kv[1]}"'
        return str

    def __repr__(self):
        return f"HTMLNode(Tags: {self.tag},\nValue: {self.value},\nChildren: {self.children},\nProps: {self.props_to_html()})"
