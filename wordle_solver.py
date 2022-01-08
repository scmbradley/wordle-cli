from wordle import Wordle, GuessStatus
from itertools import product


class WordleSolver:
    def __init__(self, wordle, word_list=None):
        self.wordle = wordle
        if word_list is None:
            self.word_list = wordle.word_list
        self.stat_dict = self.word_list.position_stats(num=wordle.size)
        self.reset_for_new_game()
        self.letter_iterator = sorted(
            product(range(26), repeat=self.wordle.size), key=sum
        )

    def reset_for_new_game(self):
        self.info_dict = dict()
        for letter in "QWERTYUIOPASDFGHJKLZXCVBNM":
            self.info_dict[letter] = set(range(self.wordle.size))
        self.letters_in_word = set()

    def guess(self, word):
        r = self.wordle.guess(word)
        self.parse_report(r)

    def solve(self):
        while self.wordle.solved is False:
            word = self.pick_word()
            self.guess(word)

    def parse_report(self, report):
        self.letters_in_word.update(report.correct_letters())
        for pos, letter_report in enumerate(report.report):
            letter, status = letter_report
            print(f"letter {letter}, status {status}")
            if (status is GuessStatus.WRONG) or (status is GuessStatus.IN_WORD):
                self.info_dict[letter].difference_update(set([pos]))
            elif status == GuessStatus.IN_POS:
                self.info_dict[letter] = set([pos])

    def pick_word(self):
        for i_list in self.letter_iterator:
            if self.validate_word(self.index_list_to_word(i_list)):
                return self.index_list_to_word(i_list)
        return False

    def index_list_to_word(self, i_list):
        word = []
        for i in range(self.wordle.size):
            word.append(self.stat_dict[i][i_list[i]])
        return "".join(word)

    def validate_word(self, word):
        for x in self.letters_in_word:
            if x not in word:
                return False
            if word.index(x) not in self.info_dict[x]:
                return False
        return word in self.word_list.word_list

    def print_info(self):
        if self.letters_in_word != []:
            for letter in self.letters_in_word:
                print(f"Letter: {letter}")
                print(",".join(self.info_dict[letter]))
        else:
            print("No information")
