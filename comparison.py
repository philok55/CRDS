from submission import Submission

class Comparison():
    # Minimum size for a sub tree to be compared
    TREE_SIZE_THRESHOLD = 2

    HL_COLOR = '\033[91m'
    STD_COLOR = '\033[0m'

    ERRORS = {
        0: 'No error in this file.',
        1: 'Error during lexing stage.',
        2: 'Error during parsing stage.'
    }

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.similarities = []
        self.similarity_score = -1
        self.s_sim_score = None
        self.t_sim_score = None
        self.error = False

    def similarity_check_ccs(self):
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
        return True

    def set_similarity_score(self):
        if self.error:
            return

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

    def print_ui(self):
        """
        Prints a simple highlighting UI to the terminal,
        displaying similarities between two files.
        """
        source_sim_lines = []
        target_sim_lines = []
        for sim in self.similarities:
            source_sim_lines += range(sim[0][0][0], sim[0][1][0] + 1)
            target_sim_lines += range(sim[1][0][0], sim[1][1][0] + 1)
        target_sim_lines = set(target_sim_lines)
        source_sim_lines = set(source_sim_lines)

        print("-----------------------------------------------------------")
        print(f"SOURCE FILE: {self.source.file}")
        print("-----------------------------------------------------------")
        print("\n")
        with open(self.source.file) as s:
            s_line_count = 0
            for i, line in enumerate(s):
                s_line_count += 1
                if i+1 in source_sim_lines:
                    print(f"{self.HL_COLOR}{line}{self.STD_COLOR}", end='')
                else:
                    print(line, end='')

        print("\n\n\n")
        print("-----------------------------------------------------------")
        print(f"TARGET FILE: {self.target.file}")
        print("-----------------------------------------------------------")
        print("\n")
        with open(self.target.file) as t:
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
        s_file_name = self.source.file.replace('\\', '/').split('/')[-1]
        t_file_name = self.target.file.replace('\\', '/').split('/')[-1]

        print("")
        if self.error:
            print(f"COMPARISON: {s_file_name} <--> {t_file_name}: ERROR")
            print(f"{s_file_name}: {self.ERRORS[self.source.error]}")
            print(f"{t_file_name}: {self.ERRORS[self.target.error]}")
            print("")
            return

        print(f"COMPARISON: {s_file_name} <--> {t_file_name}: {self.similarity_score}")
        print(f"{s_file_name}: {self.s_sim_score}%")
        print(f"{t_file_name}: {self.t_sim_score}%")
        print("")
