from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:

    new_nodes = []
    wrapped_text_type = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }[delimiter]

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
                new_nodes.append(TextNode(content, wrapped_text_type))

            if search_start_index != len(old_node.text):
                new_nodes.append(TextNode(old_node.text[search_start_index:], TextType.TEXT))

    return new_nodes

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
print(new_nodes)
