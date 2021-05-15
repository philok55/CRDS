"""Main entry point for the plagiarism checker module."""

import sys
from antlr4 import FileStream
from plagiarism_checker import PlagiarismChecker


SUPPORTED_EXTENSIONS = ['py', 'c']


def main(argv):
    ext_1 = argv[1].split('.')[-1]
    ext_2 = argv[2].split('.')[-1]

    if ext_1 != ext_2 or ext_1 not in SUPPORTED_EXTENSIONS:
        print("File types not supported.")
        return

    checker = PlagiarismChecker(argv[1], argv[2], ext_1)
    # checker.check_completely_similar()
    # checker.similarity_check_ccs()
    checker.similarity_check_new()


if __name__ == '__main__':
    main(sys.argv)
