"""Main entry point for the CRDS plagiarism checker."""

import os
import sys
from crds.crds import CRDS


SUPPORTED_EXTENSIONS = ['py', 'c']


def main(argv):
    files = []
    selected_ext = ''
    try:
        dir = os.listdir(argv[1])
        for file in dir:
            path = os.path.join(argv[1], file)
            if not os.path.isfile(path):
                print("Warning: subdirectories are not supported. Only files in the given directory are analysed.")
                continue
            ext = file.split('.')[-1]
            if ext in SUPPORTED_EXTENSIONS and selected_ext in ['', ext]:
                files.append(path)
                selected_ext = ext
            elif ext in SUPPORTED_EXTENSIONS:
                print("There are multiple file types in this directory. Please use only one programming language at once.")
                return
            else:
                print(f"File {file} skipped: file type not supported.")
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

    # files.append(files[0].replace("original", "reordered_conditionals"))

    checker = CRDS(files, selected_ext)
    checker.run()


if __name__ == '__main__':
    main(sys.argv)
