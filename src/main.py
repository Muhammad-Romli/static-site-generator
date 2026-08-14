from src.file_operator.file_operator import copy_filepath, remove_public
from src.file_operator.set_up_html import generate_pages_recursive
import sys

if sys.argv[1]:
    basepath = sys.argv[1]
else:
    basepath = "/"
def main():
    y_or_n_question = input("You sure you want to proceed? this will remove all your file in public folder? (y/n)")
    if y_or_n_question == "y":
        generate_pages_recursive("content", "template.html", 'docs', basepath)
        copy_filepath()
    elif y_or_n_question == "n":
        print("Operation Terminated")
        return
    
    else:
        print("input correctly, Operation Terminated")
        return

if __name__ == "__main__":
    main()

    
