"""
The main plagiarism checking class.
It reads the files and executes the comparison.
"""


from submission import Submission
from comparison import Comparison
import os
import psutil


class PlagiarismChecker():
    """
    The main plagiarism checking class.
    It reads the files and executes the comparison.

    Currently only between two files.
    Python and C are supported.
    """

    def __init__(self, files, extension):
        self.extension = extension
        self.files = files
        self.submissions = []
        self.comparisons = []

    def run(self):
        """Main entry for similarity check."""
        self.build_submissions()
        self.run_comparison()
        self.print_comparisons()

    def build_submissions(self):
        for file in self.files:
            ramusage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
            if ramusage > 500:
                print('RAM usage over 500MB, quitting.')
                exit()
            submission = Submission(file, self.extension)
            try:
                submission.build_hash_trees()
            except ValueError:
                pass
            self.submissions.append(submission)

    def run_comparison(self):
        done = []
        for source in self.submissions:
            done.append(source)
            for target in self.submissions:
                if target in done:
                    continue
                comp = Comparison(source, target)
                comp.similarity_check_ccs()
                comp.set_similarity_score()
                self.comparisons.append(comp)

    def print_comparisons(self):
        self.comparisons.sort(key=lambda x: x.similarity_score, reverse=True)
        for comp in self.comparisons:
            comp.print_similarity_score()
