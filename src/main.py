"""Main entry point for the static site generator.

This module defines the main entry point for the static site generator,
including the `main` function and the `text_node_to_html_node` function.
It handles the conversion of TextNode objects to LeafNode objects,
which represent HTML elements.

Usage: python main.py
"""

import shutil
from pathlib import Path

from blocks import markdown_to_html_node
from parsing import extract_title


def copy_static(src: Path, dest: Path) -> None:
    """Copies the contents from a source directory to a desination directory.

    First deletes all files from the destination directory, then makes a copy of
    all files in the source directory.

    Args:
        src: The source directory path.
        dest: The destination directory path.

    Raises:
        TypeError: If src and dest are not valid Path objects.
        ValueError: If src is not a directory or does not exist.
    """
    if not isinstance(src, Path) or not isinstance(dest, Path):
        raise TypeError("src and dest must be Path objects")
    if not src.is_dir():
        raise ValueError(f"Source path '{src}' is not a directory or does not exist.")

    # First delete everything from destination directory
    delete_files(dest)

    # copy files
    for dirpath, dirs, files in src.walk():
        relative_path = dirpath.relative_to(src)
        dest_dir = dest / relative_path
        # create all directories
        for name in dirs:
            dest_subdir = dest_dir / name
            try:
                dest_subdir.mkdir(exist_ok=True)
            except OSError as e:
                print(f"Error creating directory '{dest_subdir}': {e}")
        # copy files
        for name in files:
            src_file = dirpath / name
            dest_file = dest_dir / name
            if src_file.is_file():
                try:
                    shutil.copy(src_file, dest_file)
                except (shutil.Error, OSError) as e:
                    print(f"Error copying file '{src_file}' to '{dest_file}': {e}")


def delete_files(directory: Path) -> None:
    """Recursively deletes all files and directories in path."""
    for root, dirs, files in directory.walk(top_down=False):
        for name in files:
            (root / name).unlink()
        for name in dirs:
            (root / name).rmdir()


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    """Convert a markdown page to an html page using a specified template.

    Args:
        from_path: The path to the markdown file.
        template_path: The path to the template file.
        dest_path: The path to save the html file.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with from_path.open("rt", encoding="utf-8") as file:
        markdown = file.read()
    with template_path.open("rt", encoding="utf-8") as file:
        html = file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = html.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    # create the file and any necessary directories
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with dest_path.open("wt", encoding="utf-8") as file:
        file.write(html)


def main() -> None:
    """Entry point for the static site generator."""
    # clean public directory and copy over static files
    copy_static(Path("static"), Path("public"))
    # generate a page
    markdown = Path("content/index.md")
    template = Path("templates/template.html")
    html_file = Path("public/index.html")
    generate_page(markdown, template, html_file)


if __name__ == "__main__":
    main()
