from block_transformer import BlockType, markdown_to_block, block_to_BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_transformer import text_to_textnodes
from text_node import text_node_to_leaf_node


def markdown_to_html_node(markdown: str) -> HTMLNode: #The HTML node that gonna be returned is Grandparent
    smaller_parent_lists = []
    list_of_blocks = markdown_to_block(markdown)
    for block in list_of_blocks:
        block_type = block_to_BlockType(block)
        parent_node = block_type_to_html_nodes(block_type, block)
        smaller_parent_lists.extend(parent_node)
    grandparent_node = ParentNode("div", smaller_parent_lists)
    return grandparent_node


def text_to_children(text: str) -> list[LeafNode]: #this is LeafNode
    list_of_leaf_nodes = []
    list_of_text_nodes = text_to_textnodes(text)
    for text_node in list_of_text_nodes:
        leaf_node = text_node_to_leaf_node(text_node)
        list_of_leaf_nodes.append(leaf_node)
    return list_of_leaf_nodes



def block_type_to_html_nodes(block_type: BlockType, block: str) -> list[HTMLNode]:
    smaller_parents_list = []

    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        paragraph_text  = " ".join(lines)
        children_nodes = text_to_children(paragraph_text)
        smaller_parent_node = ParentNode("p", children_nodes)
        smaller_parents_list.append(smaller_parent_node)

    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        stripped_lines = [line[1:].strip() for line in lines]
        joined_stripped_lines = "\n".join(stripped_lines)
        children_nodes = text_to_children(joined_stripped_lines)
        quote_node = ParentNode("blockquote", children_nodes)
        smaller_parents_list.append(quote_node)

    elif block_type == BlockType.HEADING:
        count = len(block) - len(block.lstrip("#"))
        stripped_block = block[count:].strip() #this remove the "#" and the extra space
        children_nodes = text_to_children(stripped_block)
        heading_node = ParentNode(f"h{count}", children_nodes)
        smaller_parents_list.append(heading_node)

    elif block_type == BlockType.ORDERED_LIST:
        list_item_nodes = []
        lines = block.split("\n")
        for line in lines:
            item_text = line[3:].strip() #all item in unordered list md, start with "1. "  or "2. "
            item_children = text_to_children(item_text)
            li_node = ParentNode("li", item_children)
            list_item_nodes.append(li_node)
        ol_node  = ParentNode("ol", list_item_nodes)
        smaller_parents_list.append(ol_node)


    elif block_type == BlockType.UNORDERED_LIST:
        list_item_nodes = []
        lines = block.split("\n")
        for line in lines:
            item_text = line[2:] #all item in unordered list md, start with "- "  or "* "
            item_children = text_to_children(item_text)
            li_node = ParentNode("li", item_children)
            list_item_nodes.append(li_node)
        ul_node  = ParentNode("ul", list_item_nodes)
        smaller_parents_list.append(ul_node)

    elif block_type == BlockType.CODE:
        modified_code_text = block.strip("`").lstrip("\n")
        code_leaf_node = LeafNode("code", modified_code_text)
        code_parent_node = ParentNode("pre", [code_leaf_node])
        smaller_parents_list.append(code_parent_node)

    return smaller_parents_list