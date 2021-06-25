"""
A Comparison object is used to compare to Submission objects.

It contains the actual comparison algorithm that is run between two Submissions.

The CCS-based similarity check and the CRDS reordering detection are executed
in the same traversal of the submissions.
"""

from .submission import Submission
from .result import Result

class Comparison():
    """
    A Comparison object is used to compare to Submission objects.

    Call run_crds to execute the CRDS algorithm.
    """

    # Minimum size for a sub tree to be compared
    TREE_SIZE_THRESHOLD = 10

    USE_PARAM_NAMES = True

    def __init__(self, source, target):
        """
        Call __init__ with source:Submission and target:Submission
        """
        self.source = source
        self.target = target
        self.similarities = []
        self.similarity_score = -1
        self.s_sim_score = None
        self.t_sim_score = None
        self.error = False
        self.reorderings = []

    def run_crds(self, similarity_only=False):
        """
        The main CRDS comparison and decection algorithms.

        The comparison algorithm is based on the CCS paper:
        https://doi.org/10.1109/ICBNMT.2010.5705174.

        Both trees are compared in linear form,
        cross-comparing sub trees of the same size.

        Call with similarity_only=True to only execute the
        similarity checks.
        """
        if None in [self.source_tree, self.target_tree]:
            self.target.build_hash_trees()
        if (self.source.error != Submission.NO_ERROR or
            self.target.error != Submission.NO_ERROR):
            self.error = True
            return False
        for size in self.source.sizes:
            if size < self.TREE_SIZE_THRESHOLD:
                break
            if size not in self.target.sub_trees:
                continue
            for s_subtree in self.source.sub_trees[size]:
                for t_subtree in self.target.sub_trees[size]:
                    if s_subtree.hash_value != t_subtree.hash_value:
                        continue  # Subtrees are not similar

                    self.similarities.append((
                        s_subtree.get_file_location(),
                        t_subtree.get_file_location()
                    ))

                    exact_hashes_equal = s_subtree.exact_hash == t_subtree.exact_hash
                    if self.USE_PARAM_NAMES:
                        exact_hashes_equal = s_subtree.names_hash_exact == t_subtree.names_hash_exact

                    if similarity_only or exact_hashes_equal:
                        continue  # No need to look for reorderings

                    s_hashes, t_hashes, s_sub_thr, t_sub_thr = self.analyse_children(s_subtree, t_subtree)

                    if sorted(s_hashes) == sorted(t_hashes):
                        self.find_reordering(s_subtree, t_subtree)

                    self.search_sub_thr(s_sub_thr, t_sub_thr)
        return True

    def analyse_children(self, s_subtree, t_subtree):
        """
        Pre-analysis of child sub trees, before the reordering detection.

        This method returns a list of hashes of both sub trees' children.

        It also checks if any of the children are below the noise threshold,
        and returns these sorted by size in a dictionary.
        """
        s_sub_thr = {}
        t_sub_thr = {}
        s_hashes = []
        t_hashes = []
        for c in s_subtree.get_children():
            if self.USE_PARAM_NAMES:
                s_hashes.append(c.names_hash)
            else:
                s_hashes.append(c.hash_value)
            c_size = c.sub_tree_size
            if c_size <= self.TREE_SIZE_THRESHOLD:
                if c_size not in s_sub_thr:
                    s_sub_thr[c_size] = []
                s_sub_thr[c_size].append(c)

        for c in t_subtree.get_children():
            if self.USE_PARAM_NAMES:
                t_hashes.append(c.names_hash)
            else:
                t_hashes.append(c.hash_value)
            c_size = c.sub_tree_size
            if c_size <= self.TREE_SIZE_THRESHOLD:
                if c_size not in s_sub_thr:
                    continue
                if c_size not in t_sub_thr:
                    t_sub_thr[c_size] = []
                t_sub_thr[c_size].append(c)

        return s_hashes, t_hashes, s_sub_thr, t_sub_thr

    def find_reordering(self, source, target):
        """
        Find reorderings between the direct children of the subtrees
        <source> and <target>. Here we know <source> and <target> are
        equal, except for one or more reordering(s).
        """
        reordering = []
        s_children = source.get_children()
        t_children = target.get_children()

        if self.USE_PARAM_NAMES:
            s_hashes = [c.names_hash for c in s_children]
            t_hashes = [c.names_hash for c in t_children]
        else:
            s_hashes = [c.hash_value for c in s_children]
            t_hashes = [c.hash_value for c in t_children]

        for i, s_child in enumerate(s_children):
            if s_hashes[i] == t_hashes[0]:
                del t_children[0]
                del t_hashes[0]
                continue
            j = 0
            while True:
                if j >= len(t_children):
                    return  # Should not be possible
                if s_hashes[i] == t_hashes[j]:
                    t_child = t_children[j]
                    reordering.append((
                        s_child.get_file_location(),
                        t_child.get_file_location()
                    ))
                    del t_children[j]
                    del t_hashes[j]
                    break
                j += 1

        if reordering != []:
            self.reorderings.append(reordering)

    def search_sub_thr(self, s_sub_thr, t_sub_thr):
        """
        This method searches for reorderings in small subtrees
        (below the threshold). Source and target subtrees of
        the same size are cross compared using recursive tree
        traversal.
        """
        for size, s_node_list in s_sub_thr.items():
            if size not in t_sub_thr:
                continue
            for s_node in s_node_list:
                for t_node in t_sub_thr[size]:
                    self.find_recursive(s_node, t_node)

    def find_recursive(self, s_node, t_node):
        """
        Look for a reorderings anywhere between
        sub trees s_node and t_node.

        Uses recursive tree traversal.
        """
        exact_hashes_equal = s_node.exact_hash == t_node.exact_hash
        if self.USE_PARAM_NAMES:
            exact_hashes_equal = s_node.names_hash_exact == t_node.names_hash_exact

        if s_node.sub_tree_size < 3 or exact_hashes_equal:
            # Recursion base case:
            # Not enough children for a reordering,
            # or the rest of the subtree is exactly equal
            return

        s_hashes, t_hashes, s_sub_thr, t_sub_thr = self.analyse_children(s_node, t_node)

        if sorted(s_hashes) == sorted(t_hashes):
            self.find_reordering(s_node, t_node)

        self.search_sub_thr(s_sub_thr, t_sub_thr)

    def get_results(self):
        """Format and return the results of the comparison as a Result object."""
        if self.error:
            return Result(
                self.source.file,
                self.target.file,
                self.similarities,
                -1,
                None, None,
                self.source.error,
                self.target.error,
                self.reorderings
            )

        source_sim_lines = []
        target_sim_lines = []
        for sim in self.similarities:
            source_sim_lines += range(sim[0][0][0], sim[0][1][0] + 1)
            target_sim_lines += range(sim[1][0][0], sim[1][1][0] + 1)
        target_sim_lines = set(target_sim_lines)
        source_sim_lines = set(source_sim_lines)

        source_len = 0
        with open(self.source.file) as s:
            source_len = sum(1 for _ in s)

        target_len = 0
        with open(self.target.file) as t:
            target_len = sum(1 for _ in t)

        try:
            self.s_sim_score = round(len(source_sim_lines) / source_len * 100, 2)
            self.t_sim_score = round(len(target_sim_lines) / target_len * 100, 2)
            self.similarity_score = round((self.s_sim_score + self.t_sim_score) / 2, 2)
        except ZeroDivisionError:
            self.s_sim_score = 0
            self.t_sim_score = 0
            self.similarity_score = 0

        return Result(
            self.source.file,
            self.target.file,
            self.similarities,
            self.similarity_score,
            self.s_sim_score,
            self.t_sim_score,
            self.source.error,
            self.target.error,
            self.reorderings
        )
