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
        self.build_submissions()
        self.run_comparison()
        self.show_results()

    def build_submissions(self):
        for file in self.files:
            ramusage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
            if ramusage > 800:
                print(f'RAM usage: {ramusage} MB')
            submission = Submission(file, self.extension)
            submission.build_hash_trees()
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
                result = comp.get_results()
                self.results.append(result)
        # done = []
        # for source in self.files:
        #     done.append(source)
        #     s_submission = Submission(source, self.extension)
        #     for target in self.files:
        #         if target in done:
        #             continue
        #         t_submission = Submission(target, self.extension)
        #         comp = Comparison(s_submission, t_submission)
        #         comp.similarity_check_ccs()
        #         result = comp.get_results()
        #         self.results.append(result)
        #         ramusage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
        #         if ramusage > 500:
        #             print('RAM usage over 500MB, quitting.')
        #             exit()

    def show_results(self):
        self.results.sort(key=lambda x: x.similarity_score, reverse=True)
        for result in self.results:
            result.print_similarity_score()
            answer = input("Do you want to see the UI? (y/n)")
            if answer == 'y':
                result.print_ui()
