### all type of blocks that get supported on this SSG:
# - paragraph
# - heading
# - code
# - quote
# - unordered_list
# - ordered_list

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING =  "heading"
    CODE =  "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_block(markdown_text: str) -> list[str]:
    finished_list_of_blocks = []
    list_of_blocks = markdown_text.split("\n\n")
    for block in list_of_blocks:
        finished_block = block.strip()
        if finished_block == "":
            continue #this also effectively deleting it
        finished_list_of_blocks.append(finished_block)
    return finished_list_of_blocks


def block_to_BlockType(block: str) -> BlockType:
    stripped_block = block.strip()
    if stripped_block.startswith("# ") or stripped_block.startswith("## ") or stripped_block.startswith("### ") or stripped_block.startswith("#### ") or stripped_block.startswith("##### ") or stripped_block.startswith("###### "):
        return BlockType.HEADING
    
    if stripped_block.startswith("```") and stripped_block.endswith("```"):
        return BlockType.CODE
    
    for line in stripped_block.split("\n"):  #This SSG assume that every block is perfectly formatted
        if not line.startswith("> "):
            break
        return BlockType.QUOTE
    
    for line in stripped_block.split("\n"): 
        if not line.startswith("- "):
            break
        return BlockType.UNORDERED_LIST
    
    count = 0
    for line in stripped_block.split("\n"):
        count += 1
        if not line.startswith(f"{count}"):
            break
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH 

