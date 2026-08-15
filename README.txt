# Static Site Generator

A command-line tool that converts Markdown files(non programming language) into
HTML code(a programming language) that almost every website run on, this project is
so i can learn things like data pipelines, parsing, regex, and experience


## Status (COMPLETED)
🟢FULLY COMPLETED🟢
⚠️  This project is not made for fully professional and production-readdy


## Limitation
- this code not support full inline nested parsing, like **_this_**
- in a link and image url, parentheses could not be inside another parenthesis(double parenthesis)


## How to use it
- You can customize some of the configuration in main.py
- Run main.sh if you want to run it locally
- Run build.sh if you want to run it in github pages


## Tech
- Python (using only standard library without external library)
- Everything can be done offline and fast
- use main.sh to to serve the site in localhost:8888


## Flow of data
1. First, in the static folder, The index.css gonna get recursively copied to public directory, and the template.html is gonna get processsed first for the next step as template of the .md files

2. The content in the content directory which filled with .md is recursively get turned into .HTML files(this process in 2.1 to 2.5):
2.1. The Markdown file gonna  gonna get splitted into blocks, the block has it's own type, because thats how HTML work(example: code block, paragraph block, header block)
2.2. For each block is gonna get splitted into TextNodes
2.3. For each TextNode is gonna get turned into the HTMLNode
2.4. The HTMLNode gonna get turned into HTML Code depending are they ParentNode or LeafNode
2.5. Repeat this process for every .md files and copy it to docs folder(or whatever folder you want, you can customize it in main.py)


## Screenshot
