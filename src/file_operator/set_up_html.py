from src.markdown_transformer import markdown_to_html_node
import os

def extract_title(markdown: str) -> str:
    stripped_markdown = markdown.strip()
    lines = stripped_markdown.split("\n")
    for line in lines:
        if line.startswith("# "): #the space is necessary so is indicate that is h1
            return line.strip("#").strip() #stripping "#" and whitespaces
    raise Exception('make sure to put line with single "#"(h1) inside of your markdown')


def generate_page(from_path:str, template_path:str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    with open(template_path, "r", encoding="utf-8") as template:
        template_content = template.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    half_ready_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    ready_html = half_ready_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path) #if dest_path is only file is gonna return ""
    if dest_dir_path:
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as destination:
        destination.write(ready_html)

 
def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path, basepath:str):

    for content in os.listdir(dir_path_content):
        joined_dir_content_path = os.path.join(dir_path_content, content)
        if content.endswith(".md"):
            no_md_extension = content[:-3]
            html_extension_content = no_md_extension + ".html"
            joined_dest_dir_path = os.path.join(dest_dir_path, html_extension_content)
        else:
            joined_dest_dir_path = os.path.join(dest_dir_path, content)

        if os.path.isdir(joined_dir_content_path):
            generate_pages_recursive(joined_dir_content_path, template_path, joined_dest_dir_path, basepath)
        elif os.path.isfile(joined_dir_content_path):
            generate_page(joined_dir_content_path, template_path, joined_dest_dir_path, basepath) # i use joined_dest_dir_path instead of dest_dir_path because generate_page need path of file like "content/images/hello.png", instead of the parent dir
