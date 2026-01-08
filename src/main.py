from static_gen import copy_dir_static
from generate_page import gen_page_recursive

def main():
    copy_dir_static("static", "public")
    gen_page_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()