class Result():
    HL_COLOR = '\033[91m'
    STD_COLOR = '\033[0m'

    ERRORS = {
        0: 'No error in this file.',
        1: 'Error during lexing stage.',
        2: 'Error during parsing stage.'
    }

    def __init__(self,
                 source_file,
                 target_file,
                 similarities,
                 similarity_score,
                 s_sim_score,
                 t_sim_score,
                 s_error,
                 t_error):
        self.source_file = source_file
        self.target_file = target_file
        self.similarities = similarities
        self.similarity_score = similarity_score
        self.s_sim_score = s_sim_score
        self.t_sim_score = t_sim_score
        self.s_error = s_error
        self.t_error = t_error


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
        print(f"SOURCE FILE: {self.source_file}")
        print("-----------------------------------------------------------")
        print("\n")
        with open(self.source_file) as s:
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
        with open(self.target_file) as t:
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
        s_file_name = self.source_file.replace('\\', '/').split('/')[-1]
        t_file_name = self.target_file.replace('\\', '/').split('/')[-1]

        print("")
        if self.s_error > 0 or self.t_error > 0:
            print(f"COMPARISON: {s_file_name} <--> {t_file_name}: ERROR")
            print(f"{s_file_name}: {self.ERRORS[self.s_error]}")
            print(f"{t_file_name}: {self.ERRORS[self.t_error]}")
            print("")
            return

        print(f"COMPARISON: {s_file_name} <--> {t_file_name}: {self.similarity_score}")
        print(f"{s_file_name}: {self.s_sim_score}%")
        print(f"{t_file_name}: {self.t_sim_score}%")
        print("")
