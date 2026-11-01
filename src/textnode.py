import re
from enum import Enum

from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode


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
        return f'TextNode("{self.text}", TextType.{self.text_type.value}{f', {self.url}'  if self.url is not None else ""})'


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


def split_nodes_delimiter(
    old_nodes: list["TextNode"],
    delimiter: str,
    text_type: "TextType"
) -> list["TextNode"]:

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            search_start_index = 0
            while old_node.text.find(delimiter, search_start_index) != -1:
                starting_delimiter_index : int= old_node.text.find(delimiter, search_start_index)
                starting_content_index: int = starting_delimiter_index + len(delimiter)
                finishing_content_index: int = old_node.text.find(
                    delimiter,
                    starting_content_index
                )
                if finishing_content_index == -1:
                    raise Exception("No matching delimiter found, invalid Markdown")
                search_start_index: int = finishing_content_index + len(delimiter)

                preceding_text: str = old_node.text[:starting_delimiter_index]
                if preceding_text:
                    new_nodes.append(TextNode(preceding_text, TextType.TEXT))
                content = old_node.text[starting_content_index: finishing_content_index]
                new_nodes.append(TextNode(content, text_type))

            if search_start_index != len(old_node.text):
                new_nodes.append(TextNode(old_node.text[search_start_index:], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            text_to_process = old_node.text
            image_alt_and_links = extract_markdown_images(text_to_process)
            if not image_alt_and_links:
                new_nodes.append(old_node)
            else:
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
            if not link_alt_and_links:
                new_nodes.append(old_node)
            else:
                for link_alt, link in link_alt_and_links:
                    sections = text_to_process.split(f"[{link_alt}]({link})", 1)
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


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"


def block_to_block_type(markdown_block: str) -> BlockType:
    lines = markdown_block.split("\n")
    if re.fullmatch(r"^#{1,6} \w+", markdown_block, re.MULTILINE | re.DOTALL) is not None:
        return BlockType.HEADING
    elif re.fullmatch(r"^```.+?```", markdown_block, re.MULTILINE | re.DOTALL):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(
        re.match(r"^\d+?\. ", line) is not None and line.split(".", 1)[0] == str(i+1)
        for i, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def md_block_to_html_paragraph(text):
    block_text = " ".join(text.split())
    return ParentNode(
        tag="p",
        children=text_to_children(block_text)
    )


def md_block_to_html_heading(text):
    block_text = text.lstrip("# ")
    return ParentNode(
        tag=f"h{text[:6].count("#")}",
        value=text_to_children(block_text)
    )


def md_block_to_html_quote(text):
    block_text = " ".join(line.strip() for line in text.split("\n>"))
    return ParentNode(
        tag="blockquote",
        value=text_to_children(block_text)
    )


def md_block_to_html_unordered_list(text):
    line_nodes = []
    for line in text.split("\n-"):
        line_children = text_to_children(line.strip())
        line_nodes.append(ParentNode(tag="li"), children=line_children)
    return ParentNode(
        tag="ul",
        children=line_nodes
    )


def md_block_to_html_unordered_list(text):
    line_nodes = []
    for line in text.split("\n"):
        line = line.split(".", 1)[1].strip()
        line_children = text_to_children(line)
        line_nodes.append(ParentNode(tag="li"), children=line_children)
    return ParentNode(
        tag="ol",
        children=line_nodes
    )


def md_block_to_html_code(text):
    block_text = "\n".join(line.strip() for line in text.strip("` \n").split("\n") if line) + "\n"
    text_node = TextNode(block_text, TextType.CODE)
    return ParentNode(
        tag="pre",
        children=[text_node_to_html_node(text_node)]
    )


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    for block_text in markdown_blocks:
        block_type = block_to_block_type(block_text)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(md_block_to_html_paragraph(block_text))
            case BlockType.HEADING:
                children.append(md_block_to_html_heading(block_text))
            case BlockType.CODE:
                children.append(md_block_to_html_code(block_text))
            case BlockType.QUOTE:
                children.append(md_block_to_html_quote(block_text))
            case BlockType.UNORDERED_LIST:
                children.append(md_block_to_html_unordered_list(block_text))
            case BlockType.ORDERED_LIST:
                children.append(md_block_to_html_ordered_list(block_text))
    return ParentNode(tag="div", children=children)
