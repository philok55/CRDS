"""
The main plagiarism checking class.
It reads the files and executes the comparison.
"""


from antlr4 import CommonTokenStream, FileStream
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from parsers.C.CLexer import CLexer
from parsers.C.CParser import CParser
from hash_tree.tree_builders.python_tree_builder import PythonTreeBuilder
from hash_tree.tree_builders.c_tree_builder import CTreeBuilder


class PlagiarismChecker():
    """
    The main plagiarism checking class.
    It reads the files and executes the comparison.

    Currently only between two files.
    Python and C are supported.
    """

    # The supported file extensions and associated ANTLR classes
    PARSERS = {
        'py': (Python3Lexer, Python3Parser, PythonTreeBuilder),
        'c': (CLexer, CParser, CTreeBuilder)
    }

    # Minimum size for a sub tree to be compared
    TREE_SIZE_THRESHOLD = 2

    HL_COLOR = '\033[91m'
    STD_COLOR = '\033[0m'

    def __init__(self, files, extension):
        self.extension = extension
        (self.lexer, self.parser, self.tree_builder) = self.PARSERS[extension]
        self.files = files
        self.source = files[0]
        self.target = files[1]
        self.source_tree = None
        self.target_tree = None
        self.source_sub_trees = None
        self.target_sub_trees = None
        self.sizes = []
        self.similarities = []

    def run(self):
        """Main entry for similarity check."""
        for source in self.files:
            self.source = source
            for target in self.files:
                if target == source:
                    continue
                self.target = target
                self.similarity_check_ccs()
                self.print_similarity_score()

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
        source_lexer = self.lexer(FileStream(self.source))
        target_lexer = self.lexer(FileStream(self.target))

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

    def similarity_check_ccs(self):
        """
        The comparison algorithm from the CCS paper:
        https://doi.org/10.1109/ICBNMT.2010.5705174.

        Both trees are compared in linear form,
        cross-comparing sub trees of the same size.
        """
        print("----- Running CCS Similarity Check ------")
        self.similarities = []
        if None in [self.source_tree, self.target_tree]:
            self.build_hash_trees()
        for size in self.sizes:
            if size < self.TREE_SIZE_THRESHOLD:
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

    def get_similarity_score(self):
        source_sim_lines = []
        target_sim_lines = []
        for sim in self.similarities:
            source_sim_lines += range(sim[0][0][0], sim[0][1][0] + 1)
            target_sim_lines += range(sim[1][0][0], sim[1][1][0] + 1)
        target_sim_lines = set(target_sim_lines)
        source_sim_lines = set(source_sim_lines)

        source_len = 0
        with open(self.source) as s:
            source_len = sum(1 for _ in s)

        target_len = 0
        with open(self.target) as t:
            target_len = sum(1 for _ in t)

        s_sim_score = round(len(source_sim_lines) / source_len * 100, 2)
        t_sim_score = round(len(target_sim_lines) / target_len * 100, 2)
        return s_sim_score, t_sim_score

    def print_ui(self, similarities=None):
        """
        Prints a simple highlighting UI to the terminal,
        displaying similarities between two files.
        """
        if similarities is None:
            similarities = self.similarities

        source_sim_lines = []
        target_sim_lines = []
        for sim in similarities:
            source_sim_lines += range(sim[0][0][0], sim[0][1][0] + 1)
            target_sim_lines += range(sim[1][0][0], sim[1][1][0] + 1)
        target_sim_lines = set(target_sim_lines)
        source_sim_lines = set(source_sim_lines)

        print("-----------------------------------------------------------")
        print(f"SOURCE FILE: {self.source}")
        print("-----------------------------------------------------------")
        print("\n")
        with open(self.source) as s:
            s_line_count = 0
            for i, line in enumerate(s):
                s_line_count += 1
                if i+1 in source_sim_lines:
                    print(f"{self.HL_COLOR}{line}{self.STD_COLOR}", end='')
                else:
                    print(line, end='')

        print("\n\n\n")
        print("-----------------------------------------------------------")
        print(f"TARGET FILE: {self.target}")
        print("-----------------------------------------------------------")
        print("\n")
        with open(self.target) as t:
            t_line_count = 0
            for i, line in enumerate(t):
                t_line_count += 1
                if i+1 in target_sim_lines:
                    print(f"{self.HL_COLOR}{line}{self.STD_COLOR}", end='')
                else:
                    print(line, end='')

        print("\n\n\n")

        s_sim_score = round(len(source_sim_lines) / s_line_count * 100, 2)
        t_sim_score = round(len(target_sim_lines) / t_line_count * 100, 2)
        print(f"SIMILARITY IN SOURCE FILE: {s_sim_score}%")
        print(f"SIMILARITY IN TARGET FILE: {t_sim_score}%")
        print("\n")

    def print_similarity_score(self):
        """Prints the similarity score between the two analysed files."""
        s_sim_score, t_sim_score = self.get_similarity_score()

        s_file_name = self.source.replace('\\', '/').split('/')[-1]
        t_file_name = self.target.replace('\\', '/').split('/')[-1]
        print("")
        print(f"COMPARISON: {s_file_name} <--> {t_file_name}")
        print(f"{s_file_name}: {s_sim_score}%")
        print(f"{t_file_name}: {t_sim_score}%")
        print("")
