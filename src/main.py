import os
import shutil


def copy_src_dest(src="static", dest="public", top_level=False):
    if top_level and os.path.exists(dest) and os.path.isdir(dest):
        print(f"removing directory: {dest}")
        shutil.rmtree(dest)

    if not os.path.exists(dest):
        print(f"creating directory: {dest}")
        os.mkdir(dest)

    items = os.listdir(src)
    print(f"found {len(items)} items\n")
    print(*items, sep="\n")
    print("___")
    for list_item in items:
        full_path = os.path.join(src, list_item)
        if os.path.isfile(full_path):
            print(f"copying file: {full_path} - from {src} to {dest}")
            shutil.copy(full_path, dest)
        elif os.path.isdir(full_path):
            print(f"found directory: {full_path}")
            copy_src_dest(full_path, os.path.join(dest, list_item))
        print("done...\n")

    # if len(items) == 0:
    #     print("no items found, will create empty dir")
    #     os.mkdir(dest)


def main():
    copy_src_dest(top_level=True)


main()
