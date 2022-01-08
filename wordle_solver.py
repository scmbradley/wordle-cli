from wordle import Wordle, GuessStatus


class WordleSolver:
    def __init__(self, wordle, word_list=None):
        self.wordle = wordle
        if word_list is None:
            self.word_list = wordle.word_list
        self.reset_for_new_game()

    def reset_for_new_game(self):
        self.info_dict = dict()
        for letter in "QWERTYUIOPASDFGHJKLZXCVBNM":
            self.info_dict[letter] = set(range(self.wordle.size))
        self.letters_in_word = set()

    def solve(self):
        while self.wordle.solved is False:
            pass

    def parse_report(self, report):
        self.letters_in_word.update(report.correct_letters())
        for pos, letter_report in enumerate(report.report):
            letter, status = letter_report
            print(f"letter {letter}, status {status}")
            if (status is GuessStatus.WRONG) or (status is GuessStatus.IN_WORD):
                self.info_dict[letter].difference_update(set([pos]))
            elif status == GuessStatus.IN_POS:
                self.info_dict[letter] = set([pos])

    def print_info(self):
        if self.letters_in_word != []:
            for letter in self.letters_in_word:
                print(f"Letter: {letter}")
                print(",".join(self.info_dict[letter]))
        else:
            print("No information")
