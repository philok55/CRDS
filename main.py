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

    source_stream = FileStream(argv[1])
    target_stream = FileStream(argv[2])
    checker = PlagiarismChecker(source_stream, target_stream, ext_1)
    checker.similarity_check()


if __name__ == '__main__':
    main(sys.argv)
