from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str|None] | None = None
    ):
        super().__init__(tag, value, None, props)


    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


    def __repr__(self) -> str:
        tag = "" if self.tag is None else self.tag
        value = "" if self.value is None else self.value
        props = "" if self.props is None else self.props

        return (
            "LeafNode(\n"
            f"    tag={tag},\n"
            f"    value={value},\n"
            f"    props={props}\n"
            ")"

        )
