import os
import os.path as op
import shutil

from textnode import markdown_to_html_node


def copy_tree(source: str, destination: str):
    for each in os.listdir(source):
        new_source = op.join(source, each)
        new_dest = op.join(destination, each)
        if op.isfile(new_source):
            shutil.copy(new_source, new_dest)
        else:
            os.makedirs(new_dest, exist_ok=True)
            copy_tree(new_source, new_dest)


def clean_directory_and_copy_files(source: str, destination: str) -> None:
    os.makedirs(destination, exist_ok=True)
    shutil.rmtree(destination)
    copy_tree(source, destination)


def extract_title(markdown: str) -> str:
    found_header = False
    if not markdown:
        raise ValueError("Empty text")
    for line in markdown.split("\n"):
        if line[0] == "#" and line[1] != "#":
            found_header = True
            break
    if found_header:
        return line.lstrip("#").strip()
    else:
        raise Exception("No h1 header in the markdown text")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)

    full_html_page = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)

    os.makedirs(op.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html_page)



def main():
    clean_directory_and_copy_files("static", "public")
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )


if __name__ == "__main__":
    main()
