"""Creates a hashed AST the ANTLR parser. Prints the AST to "tree.txt"."""

import sys
from antlr4 import CommonTokenStream, FileStream
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from parsers.C.CLexer import CLexer
from parsers.C.CParser import CParser
from crds.tree_builders.python_tree_builder import PythonTreeBuilder
from crds.tree_builders.c_tree_builder import CTreeBuilder


SUPPORTED_EXTENSIONS = ['py', 'c']


def print_hashed_tree(argv):
    ext = argv[1].split('.')[-1]

    if ext not in SUPPORTED_EXTENSIONS:
        print("File types not supported.")
        return

    input_stream = FileStream(argv[1])

    if ext == 'py':
        lexer = Python3Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = Python3Parser(stream)
        tree = parser.file_input()
        builder = PythonTreeBuilder(tree)
    elif ext == 'c':
        lexer = CLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.compilationUnit()
        builder = CTreeBuilder(tree)

    builder.start()
    builder.print_tree(file_name="tree.txt")


if __name__ == '__main__':
    print_hashed_tree(sys.argv)
