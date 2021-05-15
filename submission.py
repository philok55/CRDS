from antlr4 import CommonTokenStream, FileStream
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from parsers.C.CLexer import CLexer
from parsers.C.CParser import CParser
from hash_tree.tree_builders.python_tree_builder import PythonTreeBuilder
from hash_tree.tree_builders.c_tree_builder import CTreeBuilder


class Submission():
    # The supported file extensions and associated ANTLR classes
    PARSERS = {
        'py': (Python3Lexer, Python3Parser, PythonTreeBuilder),
        'c': (CLexer, CParser, CTreeBuilder)
    }

    def __init__(self, file, extension):
        self.file = file
        self.extension = extension
        (self.lexer, self.parser, self.tree_builder) = self.PARSERS[extension]
        self.tree = None
        self.sub_trees = None
        self.sizes = []

    def start_parser(self, parser):
        """Start the parser by calling the (language specific) entry point."""
        if self.extension == 'py':
            return parser.file_input()
        if self.extension == 'c':
            return parser.compilationUnit()
        return None

    def build_hash_trees(self):
        """
        Preprocessing step:

        Lexer and Parser are run, ASTs are built,
        hashed and split into sorted sub trees.
        """
        lexer = self.lexer(FileStream(self.file))
        stream = CommonTokenStream(lexer)
        parser = self.parser(stream)
        tree = self.start_parser(parser)
        builder = self.tree_builder(tree)
        builder.start()
        self.tree = builder.hashed_tree
        self.sub_trees = builder.sorted_trees
        self.sizes = sorted(builder.sub_tree_sizes, reverse=True)
