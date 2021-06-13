"""
The main CRDS application class.
It reads the files and executes the comparison.
"""

from .submission import Submission
from .comparison import Comparison
import os
import psutil


class CRDS():
    """
    The main CRDS application class.
    It reads the files and executes the comparison.
    """

    MAX_RAM_USAGE_MB = 900

    def __init__(self, files, extension):
        """Expects a list of file names and a valid file extension."""
        self.extension = extension
        self.files = files
        self.submissions = []
        self.results = []

    def generate(self):
        self.build_submissions()
        self.generate_reorderings()

    def run(self):
        """Main entry for similarity check."""
        self.build_submissions()
        self.run_comparison()
        # self.print_full_results()
        # self.print_to_file()
        self.show_results()

    def build_submissions(self):
        """
        Build Submission objects for every source code file.

        Because we store every AST before the comparison, this can yield
        very high RAM usage. Set a maximum RAM usage value by changing the
        constant MAX_RAM_USAGE_MB to stop the parsing when that usage is reached.

        This is a limiting factor on the amount of submissions that can be checked at once.
        In the future it would be absolutely necessary to improve RAM performance,
        by storing the submissions to disk somehow. (TODO)
        """
        for file in self.files:
            ramusage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
            if ramusage > self.MAX_RAM_USAGE_MB:
                print(f'RAM usage: {ramusage} MB, aborting')
                print(f"Submissions parsed: {len(self.submissions)}")
                return
            submission = Submission(file, self.extension)
            submission.build_hash_trees()
            self.submissions.append(submission)

    def generate_reorderings(self):
        """
        Use the reordering generators to introduce
        reorderings in the submissions.
        """
        for file in self.files:
            ramusage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
            if ramusage > self.MAX_RAM_USAGE_MB:
                print(f'RAM usage: {ramusage} MB, aborting')
                print(f"Submissions parsed: {len(self.submissions)}")
                return
            submission = Submission(file, self.extension)
            submission.generate()

    def run_comparison(self):
        """
        Here we cross-compare all submissions.
        We build a Comparison object, run the CRDS
        algorithm and extract the results.
        """
        done = []
        for source in self.submissions:
            done.append(source)
            for target in self.submissions:
                if target in done:
                    continue
                comp = Comparison(source, target)
                comp.run_crds()
                result = comp.get_results()
                self.results.append(result)

    def show_results(self):
        """
        This is the interactive command line interface to analyse the results.

        It allows the user to go through all pairs of submissions,
        from high similarity to low, and build the UIs for every result
        on-demand (or skip through).
        """
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
        """Print all similarity results to 'results.txt'."""
        self.results.sort(key=lambda x: x.similarity_score, reverse=True)
        open("results.txt", 'w').close()

        for result in self.results:
            result.print_similarity_score(file="results.txt")

    def print_full_results(self):
        """Print all similarity results to stdout."""
        self.results.sort(key=lambda x: x.similarity_score, reverse=True)

        for result in self.results:
            result.print_similarity_score()
