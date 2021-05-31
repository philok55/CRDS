from .submission import Submission
from .result import Result
from .levenshtein import Levenshtein

class Comparison():
    # Minimum size for a sub tree to be compared
    TREE_SIZE_THRESHOLD = 10

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.similarities = []
        self.similarity_score = -1
        self.s_sim_score = None
        self.t_sim_score = None
        self.error = False
        self.reorderings = []

    def similarity_check_ccs(self, find_reordering=False):
        """
        The comparison algorithm from the CCS paper:
        https://doi.org/10.1109/ICBNMT.2010.5705174.

        Both trees are compared in linear form,
        cross-comparing sub trees of the same size.
        """
        if self.source.tree is None:
            self.source.build_hash_trees()
        if self.target.tree is None:
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
                    if s_subtree.hash_value == t_subtree.hash_value:
                        self.similarities.append((
                            s_subtree.get_file_location(),
                            t_subtree.get_file_location()
                        ))

                        if find_reordering and s_subtree.exact_hash != t_subtree.exact_hash:
                            s_leaves = {}
                            t_leaves = {}
                            s_hashes = []
                            t_hashes = []
                            for c in s_subtree.get_children():
                                s_hashes.append(c.hash_value)
                                c_size = c.sub_tree_size
                                if c_size <= self.TREE_SIZE_THRESHOLD:
                                    if c_size not in s_leaves:
                                        s_leaves[c_size] = []
                                    s_leaves[c_size].append(c)
                            
                            for c in t_subtree.get_children():
                                t_hashes.append(c.hash_value)
                                c_size = c.sub_tree_size
                                if c_size <= self.TREE_SIZE_THRESHOLD:
                                    if c_size not in s_leaves:
                                        continue
                                    if c_size not in t_leaves:
                                        t_leaves[c_size] = []
                                    t_leaves[c_size].append(c)

                            if s_hashes != t_hashes and set(s_hashes) == set(t_hashes):
                                self.find_reordering(s_subtree, t_subtree)

                            self.search_leaves(s_leaves, t_leaves)
        return True

    def get_results(self):
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

        self.s_sim_score = round(len(source_sim_lines) / source_len * 100, 2)
        self.t_sim_score = round(len(target_sim_lines) / target_len * 100, 2)
        self.similarity_score = round((self.s_sim_score + self.t_sim_score) / 2, 2)
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

    def find_reordering(self, source, target):
        reordering = []
        s_children = source.get_children()
        t_children = target.get_children()
        s_hashes = [c.hash_value for c in s_children]
        t_hashes = [c.hash_value for c in t_children]
        levenshtein = Levenshtein()
        edit_ops = levenshtein.get_ops(s_hashes, t_hashes, is_damerau=True)
        # Since we only search for reorderings, we only
        # expect 'transpose' operations here
        for op in edit_ops:
            if op[0] != 'transpose':
                continue
            s_child = s_children[op[1]]
            t_child = t_children[op[2]]
            reordering.append((
                s_child.get_file_location(),
                t_child.get_file_location()
            ))
        self.reorderings.append(reordering)

    def search_leaves(self, s_leaves, t_leaves):
        for size, s_node_list in s_leaves.items():
            if size not in t_leaves:
                continue
            for s_node in s_node_list:
                for t_node in t_leaves[size]:
                    self.find_recursive(s_node, t_node)

    def find_recursive(self, s_node, t_node):
        if s_node.sub_tree_size < 3:
            return

        reordering = []
        s_children = s_node.get_children()
        t_children = t_node.get_children()
        s_leaves = {}
        t_leaves = {}
        s_hashes = []
        t_hashes = []
        for c in s_children:
            s_hashes.append(c.hash_value)
            c_size = c.sub_tree_size
            if c_size not in s_leaves:
                s_leaves[c_size] = []
            s_leaves[c_size].append(c)
        
        for c in t_children:
            t_hashes.append(c.hash_value)
            c_size = c.sub_tree_size
            if c_size not in s_leaves:
                continue
            if c_size not in t_leaves:
                t_leaves[c_size] = []
            t_leaves[c_size].append(c)

        if set(s_hashes) == set(t_hashes):
            levenshtein = Levenshtein()
            edit_ops = levenshtein.get_ops(s_hashes, t_hashes, is_damerau=True)
            # Since we only search for reorderings, we only
            # expect 'transpose' operations here
            for op in edit_ops:
                if op[0] != 'transpose':
                    continue
                s_child = s_children[op[1]]
                t_child = t_children[op[2]]
                reordering.append((
                    s_child.get_file_location(),
                    t_child.get_file_location()
                ))
            self.reorderings.append(reordering)

        self.search_leaves(s_leaves, t_leaves)
