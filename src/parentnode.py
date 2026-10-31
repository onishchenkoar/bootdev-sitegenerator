from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)


    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("The node should have a tag")
        if not self.children:
            raise ValueError("The node should have child elements")

        children_html = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
