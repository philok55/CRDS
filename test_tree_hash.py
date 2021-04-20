"""Creates a hashed AST from python3.6 code using the ANTLR parser."""

import sys
from antlr4 import CommonTokenStream, FileStream
from antlr4.tree.Trees import Trees
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from hash_tree_builder import HashTreeBuilder


def print_hashed_tree(argv):
    input_stream = FileStream(argv[1])
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()
    builder = HashTreeBuilder(tree)
    builder.start()
    builder.print_tree(file_name="tree.txt")


if __name__ == '__main__':
    print_hashed_tree(sys.argv)
