from src.markdown_transformer import markdown_to_html_node
import os

def extract_title(markdown: str) -> str:
    stripped_markdown = markdown.strip()
    lines = stripped_markdown.split("\n")
    for line in lines:
        if line.startswith("# "): #the space is necessary so is indicate that is h1
            return line.strip("#").strip() #stripping "#" and whitespaces
    raise Exception('make sure to put line with single "#"(h1) inside of your markdown')


def generate_page(from_path:str, template_path:str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using tesmplate {template_path}")
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    with open(template_path, "r", encoding="utf-8") as template:
        template_content = template.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    half_ready_html = template_content.replace("{{ Title }}", title)
    ready_html = half_ready_html.replace("{{ Content }}", html_content)

    dest_path_parent = os.path.dirname(dest_path) #if dest_path is only file is gonna return ""
    if dest_path_parent:
        os.makedirs(dest_path_parent, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as destination:
        destination.write(ready_html)

