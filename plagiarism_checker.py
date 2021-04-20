from antlr4 import CommonTokenStream
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from hash_tree.hash_tree_builder import HashTreeBuilder


class PlagiarismChecker():
    """Between 2 files for now."""

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.source_tree = None
        self.target_tree = None

    def build_hash_trees(self):
        source_lexer = Python3Lexer(self.source)
        target_lexer = Python3Lexer(self.target)

        source_stream = CommonTokenStream(source_lexer)
        target_stream = CommonTokenStream(target_lexer)

        source_parser = Python3Parser(source_stream)
        target_parser = Python3Parser(target_stream)

        source_tree = source_parser.file_input()
        target_tree = target_parser.file_input()

        source_builder = HashTreeBuilder(source_tree)
        target_builder = HashTreeBuilder(target_tree)

        source_builder.start()
        target_builder.start()

        self.source_tree = source_builder.hashed_tree
        self.target_tree = target_builder.hashed_tree

    def check_completely_similar(self):
        print("----- Running Similarity Check ------")
        if None in [self.source_tree, self.target_tree]:
            self.build_hash_trees()
        if self.source_tree.hash_value == self.target_tree.hash_value:
            print("These files are 100% structurally similar.")
        else:
            print("There are structural differences between these files.")
