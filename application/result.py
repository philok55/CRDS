import filecmp
import json
from jinja2 import Template

class Result():
    ERRORS = {
        0: 'No error in this file.',
        1: 'Error during lexing stage.',
        2: 'Error during parsing stage.'
    }
    TEMPLATE_FILE = "ui_template.html"
    SIMILARITIES = 'sim'
    REORDERINGS = 'reo'
    OUT_FILES = {"sim": "sim_results.html", "reo": "reo_results.html"}

    def __init__(self,
                 source_file,
                 target_file,
                 similarities,
                 similarity_score,
                 s_sim_score,
                 t_sim_score,
                 s_error,
                 t_error,
                 reorderings):
        self.source_file = source_file
        self.target_file = target_file
        self.similarities = similarities
        self.similarity_score = similarity_score
        self.s_sim_score = s_sim_score
        self.t_sim_score = t_sim_score
        self.s_error = s_error
        self.t_error = t_error
        self.reorderings = reorderings

    def render_ui(self):
        """
        Renders a simple highlighting UI to HTML,
        displaying similarities between two files.
        """
        source_lines = []
        target_lines = []
        for sim in self.similarities:
            source_lines += range(sim[0][0][0], sim[0][1][0] + 1)
            target_lines += range(sim[1][0][0], sim[1][1][0] + 1)
        target_lines = set(target_lines)
        source_lines = set(source_lines)

        with open(self.TEMPLATE_FILE) as f:
            template = Template(f.read())

        with open(self.source_file) as s, open(self.target_file) as t:
            outputHTML = template.render(
                source_file_name=self.source_file,
                target_file_name=self.target_file,
                source_lines=source_lines,
                target_lines=target_lines,
                source_file=s,
                target_file=t,
                s_sim_score=self.s_sim_score,
                t_sim_score=self.t_sim_score,
                mode=self.SIMILARITIES
            )

        out_file = self.OUT_FILES[self.SIMILARITIES]
        with open(out_file, 'w') as f:
            f.write(outputHTML)

    def render_reorderings(self):
        """
        Renders a simple highlighting UI to a HTML file,
        displaying reorderings between two files.
        """
        reorderings = []
        for reorder in self.reorderings:
            s_sw_lines = []
            t_sw_lines = []
            for switch in reorder:
                s_sw_lines += range(switch[0][0][0], switch[0][1][0] + 1)
                t_sw_lines += range(switch[1][0][0], switch[1][1][0] + 1)
            reorderings.append([list(set(s_sw_lines)), list(set(t_sw_lines))])

        with open(self.TEMPLATE_FILE) as f:
            template = Template(f.read())

        with open(self.source_file) as s, open(self.target_file) as t:
            outputHTML = template.render(
                source_file_name=self.source_file,
                target_file_name=self.target_file,
                reorderings=json.dumps(reorderings),
                source_file=s,
                target_file=t,
                s_sim_score=self.s_sim_score,
                t_sim_score=self.t_sim_score,
                mode=self.REORDERINGS
            )

        out_file = self.OUT_FILES[self.REORDERINGS]
        with open(out_file, 'w') as f:
            f.write(outputHTML)

    def print_similarity_score(self):
        """Prints the similarity score between the two analysed files."""
        s_file_name = self.source_file.replace('\\', '/').split('/')[-1]
        t_file_name = self.target_file.replace('\\', '/').split('/')[-1]
        equal = False
        if filecmp.cmp(self.source_file, self.target_file):
            equal=True

        print("")
        if self.s_error > 0 or self.t_error > 0:
            print(f"COMPARISON: {s_file_name} <--> {t_file_name}: ERROR")
            print(f"{s_file_name}: {self.ERRORS[self.s_error]}")
            print(f"{t_file_name}: {self.ERRORS[self.t_error]}")
            print("")
            return

        if equal:
            print(f"COMPARISON: {s_file_name} <--> {t_file_name}: {self.similarity_score}% (EQUAL)")
        else:
            print(f"COMPARISON: {s_file_name} <--> {t_file_name}: {self.similarity_score}%")
        print(f"{s_file_name}: {self.s_sim_score}%    ", end='')
        print(f"{t_file_name}: {self.t_sim_score}%")
        print("")

    def print_to_file(self):
        """
        Append the similarity score between the
        two analysed files to the results file.
        """
        s_file_name = self.source_file.replace('\\', '/').split('/')[-1]
        t_file_name = self.target_file.replace('\\', '/').split('/')[-1]
        results_file = "results.txt"
        equal = False
        if filecmp.cmp(self.source_file, self.target_file):
            equal=True

        with open(results_file, 'a') as file:
            file.write("\n")
            if self.s_error > 0 or self.t_error > 0:
                file.write(f"COMPARISON: {s_file_name} <--> {t_file_name}: ERROR\n")
                file.write(f"{s_file_name}: {self.ERRORS[self.s_error]}    ")
                file.write(f"{t_file_name}: {self.ERRORS[self.t_error]}\n")
                file.write("\n")
                return

            if equal:
                file.write(f"COMPARISON: {s_file_name} <--> {t_file_name}: {self.similarity_score}% (EQUAL)\n")
            else:
                file.write(f"COMPARISON: {s_file_name} <--> {t_file_name}: {self.similarity_score}%\n")
            file.write(f"{s_file_name}: {self.s_sim_score}%    ")
            file.write(f"{t_file_name}: {self.t_sim_score}%\n")
