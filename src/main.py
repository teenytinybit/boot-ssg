import sys

from page_generator import copy_src_dest, generate_pages_recursive


def main():
    copy_src_dest(top_level=True)
    try:
        generate_pages_recursive("content", "template.html", "public")
    except Exception:
        print("Encountered an error. Stopping.")
        sys.exit(1)


main()
