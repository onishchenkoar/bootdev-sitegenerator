class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self) -> str:
        raise NotImplementedError("This method should overridden by child classes")


    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join(f'{prop}="{value}"' for prop, value in self.props.items())


    def __repr__(self) -> str:
        tag = "" if self.tag is None else self.tag
        value = "" if self.value is None else self.value
        children = "" if self.children is None else self.children
        props = "" if self.props is None else self.props
        
        return (
            "HTMLNode(\n"
            f"    tag={tag},\n"
            f"    value={value},\n"
            f"    children={children},\n"
            f"    props={props}\n"
            ")"
        )