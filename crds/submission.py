"""
Representation object for a single submission (source code file).

It builds and holds the generated hashed AST and the collection of sub trees.
"""

from antlr4 import CommonTokenStream, FileStream
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from parsers.C.CLexer import CLexer
from parsers.C.CParser import CParser
from reordering_generators.python_generator import PythonGenerator
from reordering_generators.c_generator import CGenerator
from .tree_builders.python_tree_builder import PythonTreeBuilder
from .tree_builders.c_tree_builder import CTreeBuilder


class Submission():
    """
    Representation class for a single submission (source code file).

    It builds and holds the generated hashed AST and the collection of sub trees.
    """

    # The supported file extensions and associated ANTLR classes
    PARSERS = {
        'py': (Python3Lexer, Python3Parser, PythonTreeBuilder, PythonGenerator),
        'c': (CLexer, CParser, CTreeBuilder, CGenerator)
    }

    NO_ERROR = 0
    LEXER_ERROR = 1
    PARSER_ERROR = 2

    def __init__(self, file, extension):
        self.file = file
        self.extension = extension
        (self.lexer, self.parser, self.tree_builder, self.generator) = self.PARSERS[extension]
        self.tree = None
        self.sub_trees = None
        self.sizes = []
        self.error = self.NO_ERROR
        self.build_hash_trees()

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
        try:
            lexer = self.lexer(FileStream(self.file))
            stream = CommonTokenStream(lexer)
            parser = self.parser(stream)
            tree = self.start_parser(parser)
            builder = self.tree_builder(tree)
            builder.start()
            self.tree = builder.hashed_tree
            self.sub_trees = builder.sorted_trees
            self.sizes = sorted(builder.sub_tree_sizes, reverse=True)
        except UnicodeDecodeError:
            self.error = self.LEXER_ERROR

    def generate(self):
        """Use the reordering generator to introduce reorderings."""
        try:
            lexer = self.lexer(FileStream(self.file))
            stream = CommonTokenStream(lexer)
            parser = self.parser(stream)
            tree = self.start_parser(parser)
            generator = self.generator(tree, self.file)
            generator.start()
        except UnicodeDecodeError:
            self.error = self.LEXER_ERROR
