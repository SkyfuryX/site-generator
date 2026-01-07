from static_gen import copy_dir_static
from generate_page import generate_page

def main():
    copy_dir_static("static", "public")
    
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()