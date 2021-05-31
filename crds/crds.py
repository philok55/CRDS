"""
The main plagiarism checking class.
It reads the files and executes the comparison.
"""


from .submission import Submission
from .comparison import Comparison
import os
import psutil


class CRDS():
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
        self.print_to_file()
        self.show_results()

    def build_submissions(self):
        for file in self.files:
            ramusage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
            if ramusage > 200:
                print(f'RAM usage: {ramusage} MB')
                print(f"Submissions parsed: {len(self.submissions)}")
                return
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
                comp.similarity_check_ccs(find_reordering=True)
                result = comp.get_results()
                self.results.append(result)

    def show_results(self):
        self.results.sort(key=lambda x: x.similarity_score, reverse=True)
        i = 0
        while True:
            if i >= len(self.results):
                return
            self.results[i].print_similarity_score()
            step = input(
                "Select an action (press letter and then enter): \n\n\
                 u = Render Similarities to sim_results.html \n\
                 r = Render Reorderings to reo_results.html \n\
                 b = Render both UIs to HTML \n\
                 n = Go to next submission \n\
                 p = Go to previous submission \n\
                 q = Quit\n")
            if step == 'p':
                if i == 0:
                    print("\nThis is the first submission.")
                else:
                    i -= 1
            elif step == 'u':
                self.results[i].render_ui()
            elif step == 'r':
                self.results[i].render_reorderings()
            elif step == 'b':
                self.results[i].render_ui()
                self.results[i].render_reorderings()
            elif step in ['n', '']:
                i += 1
            elif step == 'q':
                return
            else:
                print("\nInvalid input.")

    def print_to_file(self):
        self.results.sort(key=lambda x: x.similarity_score, reverse=True)
        open("results.txt", 'w').close()

        for result in self.results:
            result.print_to_file()
