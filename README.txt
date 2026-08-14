# Static Site Generator

A command-line tool that converts Markdown files into static HTML websites, 
built as part of the boot.dev backend curriculum.

## Status (ONGOING)
🚧 In progress — currently working on the block after doing the inline
⚠️  This project is not made for fully professional and production-readdy

## Limitation
- this code not support full inline nested parsing, like **_this_**
- in a link and image url, parentheses could not be inside another parenthesis

## What it does
- Parses Markdown text into a tree of custom node objects (TextNode, HTMLNode)
- Converts inline markdown (bold, italic, code, links, images) into HTML nodes
- (Coming soon) Fully converts full markdown documents into HTML pages

## Tech
- Python (using only standard library without external library)

## Flow of work
1. First the markdown files gonna get break list of TextNode, this step gonna be do block by block first, not all block at once
2. The next step is the block(list of TextNode), gonna be turned into a HTMLNode 
