import sys

from page_generator import copy_src_dest, generate_page


def main():
    copy_src_dest(top_level=True)
    try:
        generate_page("content/index.md", "template.html", "public/index.html")
    except Exception:
        print("Encountered an error. Stopping.")
        sys.exit(1)


main()
