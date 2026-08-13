import re
from text_node import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    valid_delimiter = ("`", "**", "_")
    finished_list = []
    if delimiter not in valid_delimiter:
        raise Exception(f"delimiter does not exist")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            finished_list.append(node)
            continue
        if delimiter not in node.text:
            finished_list.append(node)
            continue
        splitted_nodes = node.text.split(delimiter)

        for i in range(len(splitted_nodes)):
            if splitted_nodes[i] == "":
                continue
            if i % 2 == 0:
                finished_list.append(TextNode(splitted_nodes[i], TextType.TEXT))
            else:
                finished_list.append(TextNode(splitted_nodes[i], text_type))
            
    return finished_list


def text_to_textnodes(text: str) -> list[TextNode]:
    first = split_nodes_image([TextNode(text, TextType.TEXT)])
    second = split_nodes_link(first)
    third = split_nodes_delimiter(second, "`", TextType.CODE)
    fourth = split_nodes_delimiter(third, "**", TextType.BOLD)
    fifth = split_nodes_delimiter(fourth, "_", TextType.ITALIC)
    return fifth
    


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" #example of the image text:
    return re.findall(pattern, text) #"This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" #example of the link text:
    return re.findall(pattern, text) #"this is text with a link [to youtube](https://www.youtube.com/@FrostDiamond)"


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    splitted_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            splitted_nodes.append(node)
            continue
        
        extracted_alt_url = extract_markdown_images(node.text)
        if len(extracted_alt_url) == 0:
            splitted_nodes.append(node)
            continue

        remaining_text = node.text
        for pair in extracted_alt_url:
            alt, url = pair
            pair_str = f"![{alt}]({url})"
            img_node = TextNode(alt, TextType.IMAGE, url)
            splitted_text = remaining_text.split(pair_str, 1) #splitted become 2 usually unless the pair appear twice, thats why i limit to 1 to make it work

            if splitted_text[0] != "":
                splitted_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            splitted_nodes.append(img_node)

            remaining_text = splitted_text[1]
        if splitted_text[1] != "": #type: ignore
                splitted_nodes.append(TextNode(splitted_text[1], TextType.TEXT))#type: ignore | dont worry the upper check guarantee that either splitted_nodes and splitted_text exist or it never reach inner loop
    return splitted_nodes



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    splitted_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            splitted_nodes.append(node)
            continue
        
        extracted_alt_url = extract_markdown_links(node.text)
        if len(extracted_alt_url) == 0:
            splitted_nodes.append(node)
            continue

        remaining_text = node.text
        for pair in extracted_alt_url:
            alt, url = pair
            pair_str = f"[{alt}]({url})" 
            link_node = TextNode(alt, TextType.LINK, url)
            splitted_text = remaining_text.split(pair_str, 1) #splitted become 2 usually unless the pair appear twice, thats why i limit to 1 so is can work

            if splitted_text[0] != "":
                splitted_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            splitted_nodes.append(link_node)

            remaining_text = splitted_text[1]
        if splitted_text[1] != "": #type: ignore
            splitted_nodes.append(TextNode(splitted_text[1], TextType.TEXT)) #type: ignore | dont worry the upper check guarantee that either splitted_nodes and splitted_text exist or it never reach inner loop
    return splitted_nodes
