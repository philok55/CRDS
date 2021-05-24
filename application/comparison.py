from .submission import Submission
from .result import Result

class Comparison():
    # Minimum size for a sub tree to be compared
    TREE_SIZE_THRESHOLD = 7

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
                            s_children = [c.hash_value for c in s_subtree.get_children()]
                            t_children = [c.hash_value for c in t_subtree.get_children()]
                            if s_children != t_children and set(s_children) == set(t_children):
                                self.find_reordering(s_subtree, t_subtree)
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
                self.target.error
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
        matched = []
        s_children = source.get_children()
        t_children = target.get_children()
        for i, s_child in enumerate(s_children):
            for j, t_child in enumerate(t_children):
                if j in matched:
                    continue
                if s_child.hash_value == t_child.hash_value:
                    if i != j:
                        # add reordering
                        reordering.append((
                            s_child.get_file_location(),
                            t_child.get_file_location()
                        ))
                    # save index
                    matched.append(j)
                    break
        self.reorderings.append(reordering)

    def levenshteinDistance(self, s1, s2):
        """
        Levenshtein Distance between two lists.
        Nice Dynamic Programming solution from source:
        https://stackoverflow.com/a/32558749
        """
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]
