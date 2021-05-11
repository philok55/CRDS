from antlr4 import CommonTokenStream
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from parsers.C.CLexer import CLexer
from parsers.C.CParser import CParser
from hash_tree.tree_builders.python_tree_builder import PythonTreeBuilder
from hash_tree.tree_builders.c_tree_builder import CTreeBuilder


class PlagiarismChecker():
    """Between 2 files for now."""

    PARSERS = {
        'py': (Python3Lexer, Python3Parser, PythonTreeBuilder), 
        'c': (CLexer, CParser, CTreeBuilder)
    }

    def __init__(self, source, target, extension):
        self.extension = extension
        (self.lexer, self.parser, self.tree_builder) = self.PARSERS[extension]
        self.source = source
        self.target = target
        self.source_tree = None
        self.target_tree = None
        self.source_sub_trees = None
        self.target_sub_trees = None
        self.sizes = []
        self.similarities = []

    def start_parser(self, parser):
        if self.extension == 'py':
            return parser.file_input()
        if self.extension == 'c':
            return parser.compilationUnit()
        return None

    def build_hash_trees(self):
        source_lexer = self.lexer(self.source)
        target_lexer = self.lexer(self.target)

        source_stream = CommonTokenStream(source_lexer)
        target_stream = CommonTokenStream(target_lexer)

        source_parser = self.parser(source_stream)
        target_parser = self.parser(target_stream)

        source_tree = self.start_parser(source_parser)
        target_tree = self.start_parser(target_parser)

        source_builder = self.tree_builder(source_tree)
        target_builder = self.tree_builder(target_tree)

        source_builder.start()
        target_builder.start()

        self.source_tree = source_builder.hashed_tree
        self.target_tree = target_builder.hashed_tree

        self.source_sub_trees = source_builder.sorted_trees
        self.target_sub_trees = target_builder.sorted_trees

        self.sizes = sorted(source_builder.sub_tree_sizes, reverse=True)

    def check_completely_similar(self):
        print("----- Running Similarity Check ------")
        if None in [self.source_tree, self.target_tree]:
            self.build_hash_trees()
        if self.source_tree.exact_hash == self.target_tree.exact_hash:
            print("These files are 100% structurally similar, without reorderings.")
        elif self.source_tree.hash_value == self.target_tree.hash_value:
            print("These files are 100% structurally similar.")
        else:
            print("There are structural differences between these files.")

    def similarity_check(self):
        if None in [self.source_tree, self.target_tree]:
            self.build_hash_trees()
        for size in self.sizes:
            if size <= 5:
                break
            if size not in self.target_sub_trees:
                continue
            for s_subtree in self.source_sub_trees[size]:
                for t_subtree in self.target_sub_trees[size]:
                    if s_subtree.hash_value == t_subtree.hash_value:
                        self.similarities.append((
                            s_subtree.get_file_location(),
                            t_subtree.get_file_location()
                        ))

        print(self.similarities)
