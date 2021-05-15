"""Main entry point for the plagiarism checker module."""

import os
import sys
from antlr4 import FileStream
from plagiarism_checker import PlagiarismChecker


SUPPORTED_EXTENSIONS = ['py', 'c']


def main(argv):
    files = []
    selected_ext = ''
    try:
        dir = os.listdir(argv[1])
        for file in dir:
            path = os.path.join(argv[1], file)
            if os.path.isfile(path):
                ext = file.split('.')[-1]
                if ext in SUPPORTED_EXTENSIONS and selected_ext in ['', ext]:
                    files.append(path)
                    selected_ext = ext
                elif ext in SUPPORTED_EXTENSIONS:
                    print("There are multiple file types in this directory. Please use only one programming language at once.")
                    return
                else:
                    print(f"File {file} skipped: file type not supported.")
            else:
                print("Warning: subdirectories are not supported. Only files in the given directory are analysed.")
    except NotADirectoryError:
        if len(argv) < 3:
            print("Please select more than one file.")
            return
        for file in argv[1:]:
            ext = file.split('.')[-1]
            if ext in SUPPORTED_EXTENSIONS and selected_ext in ['', ext]:
                files.append(file)
                selected_ext = ext
            elif ext in SUPPORTED_EXTENSIONS:
                print("You have selected multiple file types. Please use only one programming language at once.")
                return
            else:
                print(f"File {file} skipped: file type not supported.")

    checker = PlagiarismChecker(files, selected_ext)
    checker.run()
    # checker.similarity_check_ccs()
    # checker.similarity_check_new()

    # checker.print_ui()
    # checker.print_similarity_score()


if __name__ == '__main__':
    main(sys.argv)
