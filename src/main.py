from static_gen import copy_dir_static
from generate_page import gen_page_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else: basepath = "/"
    copy_dir_static("static", "docs")
    gen_page_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()