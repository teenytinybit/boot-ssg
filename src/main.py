import sys

from page_generator import copy_src_dest, generate_pages_recursive


def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    print(f"basepath: {basepath}")
    copy_src_dest("static", "docs", top_level=True)
    try:
        generate_pages_recursive("content", "template.html", "docs", basepath)
    except Exception:
        print("Encountered an error. Stopping.")
        sys.exit(1)


main()
