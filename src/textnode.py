import re
from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f'TextNode("{self.text}", TextType.{self.text_type.value}, {self.url if self.url is not None else ""})'


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise TypeError(f"The node cannot be of the {text_node.text_type} type")


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.+?)\]\((.+?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!\!)\[(.+?)\]\((.+?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            text_to_process = old_node.text
            image_alt_and_links = extract_markdown_images(text_to_process)
            for image_alt, image_link in image_alt_and_links:
                sections = text_to_process.split(f"![{image_alt}]({image_link})", 1)
                if len(sections) == 2:
                    node_text, text_to_process = sections
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if len(sections) == 1:
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                    text_to_process = sections[0]
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            text_to_process = old_node.text
            link_alt_and_links = extract_markdown_links(text_to_process)
            for link_alt, link in link_alt_and_links:
                sections = text_to_process.split(f"[{link_alt}]({link})", 1)
                print(sections)
                if len(sections) == 2:
                    node_text, text_to_process = sections
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
                    new_nodes.append(TextNode(link_alt, TextType.LINK, link))
                if len(sections) == 1:
                    new_nodes.append(TextNode(link_alt, TextType.LINK, link))
                    text_to_process = sections[0]
    return new_nodes


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes
