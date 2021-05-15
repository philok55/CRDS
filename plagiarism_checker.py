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
        self.results = []

    def run(self):
        """Main entry for similarity check."""
        self.run_comparison()
        self.print_results()

    def run_comparison(self):
        done = []
        for source in self.files:
            done.append(source)
            s_submission = Submission(source, self.extension)
            for target in self.files:
                if target in done:
                    continue
                t_submission = Submission(target, self.extension)
                comp = Comparison(s_submission, t_submission)
                comp.similarity_check_ccs()
                result = comp.get_results()
                self.results.append(result)
                del t_submission
                del comp
                ramusage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
                if ramusage > 500:
                    print('RAM usage over 500MB, quitting.')
                    exit()

    def print_results(self):
        self.results.sort(key=lambda x: x.similarity_score, reverse=True)
        for result in self.results:
            result.print_similarity_score()
