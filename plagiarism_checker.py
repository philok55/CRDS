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
    TREE_SIZE_THRESHOLD = 4

    HL_COLOR = '\033[91m'
    STD_COLOR = '\033[0m'
 
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

    def check_completely_similar(self):
        """Checks full similarity of two files by only comparing the root nodes."""
        print("----- Running 100% Similarity Check ------")
        if None in [self.source_tree, self.target_tree]:
            self.build_hash_trees()
        if self.source_tree.exact_hash == self.target_tree.exact_hash:
            print("These files are 100% structurally similar, without reorderings.")
        elif self.source_tree.hash_value == self.target_tree.hash_value:
            print("These files are 100% structurally similar.")
        else:
            print("There are structural differences between these files.")

    def similarity_check_ccs(self):
        """
        The comparison algorithm from the CCS paper:
        https://doi.org/10.1109/ICBNMT.2010.5705174.

        Both trees are compared in linear form, 
        cross-comparing sub trees of the same size.
        """
        print("----- Running CCS Similarity Check ------")
        similarities = []
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
                        similarities.append((
                            s_subtree.get_file_location(),
                            t_subtree.get_file_location()
                        ))
        self.print_ui(similarities=similarities)

    def similarity_check_new(self):
        """
        Alternative implementation to CCS.
        
        We traverse the source tree, and use the same hash comparison as CCS.
        By only using one linearised tree, we can skip subtrees that are within
        an already matched tree.
        """
        print("----- Running Philo's Similarity Check ------")
        if None in [self.source_tree, self.target_tree]:
            self.build_hash_trees()
        self.preorder_search(self.source_tree)
        self.print_ui()

    def preorder_search(self, current):
        """The recursive traversal of our algorithm."""
        size = current.sub_tree_size
        if size in self.target_sub_trees:
            targets = self.target_sub_trees[size]
            for target in targets:
                if current.hash_value == target.hash_value:
                    self.similarities.append((
                        current.get_file_location(),
                        target.get_file_location()
                    ))
                    # No need to search children for similarity check.
                    # This is the point to look for clues within these similar subtrees.
                    # Here we will check if the hash_exact values are the same,
                    # and if they are not, look further.
                    return
        if current.sub_tree_size < self.TREE_SIZE_THRESHOLD:
            return  # Don't match sub trees that are too small
        for child in current.children:
            self.preorder_search(child)

    def print_ui(self, similarities=None):
        """
        Prints a simple highlighting UI to the terminal, 
        displaying similarities between two files.
        """
        if similarities is None:
            similarities = self.similarities

        print("-----------------------------------------------------------")
        print(f"SOURCE FILE: {self.source}")
        print("-----------------------------------------------------------")
        print("\n")
        with open(self.source) as s:
            sim_active = False
            next_sim = 0
            for i, line in enumerate(s):
                if not sim_active:
                    if next_sim < len(similarities):
                        sim = similarities[next_sim][0]
                    sim_active = True
                if i >= sim[0][0]-1 and i <= sim[1][0]-1:
                    print(f"{self.HL_COLOR}{line}{self.STD_COLOR}", end='')
                    if i == sim[1][0]-1:
                        sim_active = False
                        next_sim += 1
                else:
                    print(line, end='')

        print("\n\n\n")
        print("-----------------------------------------------------------")
        print(f"TARGET FILE: {self.target}")
        print("-----------------------------------------------------------")
        print("\n")
        with open(self.target) as t:
            sim_active = False
            next_sim = 0
            for i, line in enumerate(t):
                if not sim_active:
                    if next_sim < len(similarities):
                        sim = similarities[next_sim][1]
                    sim_active = True
                if i >= sim[0][0]-1 and i <= sim[1][0]-1:
                    print(f"{self.HL_COLOR}{line}{self.STD_COLOR}", end='')
                    if i == sim[1][0]-1:
                        sim_active = False
                        next_sim += 1
                else:
                    print(line, end='')
        
        print("\n\n\n")
