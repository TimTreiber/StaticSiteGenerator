from conversions import *
import os
import shutil

def main():
    static_to_public()
    pwd = "/home/timtreiber/GitHub/StaticSiteGenerator"
    generate_pages_recursive(f"{pwd}/content", f"{pwd}/template.html", f"{pwd}/public")

def static_to_public():
    shutil.rmtree("/home/timtreiber/GitHub/StaticSiteGenerator/public")
    shutil.copytree("/home/timtreiber/GitHub/StaticSiteGenerator/static/", "/home/timtreiber/GitHub/StaticSiteGenerator/public")

def extract_title(markdown):
    lines = (markdown.strip()).split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("missing header h1")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md_contents = f.read()
    with open(template_path) as g:
        template_contents = g.read()
    node = markdown_to_html_node(md_contents)
    html = node.to_html()
    title = extract_title(md_contents)
    template_contents = template_contents.replace('{{ Title }}', title)
    template_contents = template_contents.replace('{{ Content }}', html)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    with open(f"{dest_path}/index.html", mode = 'x') as d:
        d.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.isfile(dir_path_content):
        ls = os.listdir(dir_path_content)
        for path in ls:
            new_path = os.path.join(dir_path_content, path)
            if os.path.isfile(new_path):
                generate_page(new_path, template_path, dest_dir_path)
            if not os.path.isfile(new_path):
                generate_pages_recursive(new_path, template_path, os.path.join(dest_dir_path, path))

if __name__ == "__main__":
    main()
