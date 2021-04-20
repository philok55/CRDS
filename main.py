import sys
from antlr4 import FileStream
from plagiarism_checker import PlagiarismChecker


def main(argv):
    source_stream = FileStream(argv[1])
    target_stream = FileStream(argv[2])
    checker = PlagiarismChecker(source_stream, target_stream)
    checker.check_completely_similar()


if __name__ == '__main__':
    main(sys.argv)
