from wordle import GuessStatus


class WordleSolver:
    def __init__(self, wordle, wl_obj=None):
        self.wordle = wordle
        if wl_obj is None:
            self.wl_obj = wordle.word_list
        self.stat_dict = self.wl_obj.position_stats(num=wordle.size)
        self.reset_for_new_game()
        self.remaining_words = sorted(self.wl_obj.word_list, key=self.score_word)

    def reset_for_new_game(self):
        self.possibilities_dict = dict()
        for letter in "QWERTYUIOPASDFGHJKLZXCVBNM":
            self.possibilities_dict[letter] = set(range(self.wordle.size))
        self.letters_in_word = set()
        self.in_pos_letters = dict()

    def new_game(self, **kwargs):
        self.reset_for_new_game()
        self.wordle.new_game(**kwargs)

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
            if status is GuessStatus.WRONG:
                self.possibilities_dict[letter] = set()
            elif status is GuessStatus.IN_WORD:
                self.possibilities_dict[letter].difference_update(set([pos]))
            elif status == GuessStatus.IN_POS:
                self.in_pos_letters[pos] = letter

    def pick_word(self):
        while len(self.remaining_words) > 0:
            word = self.remaining_words.pop(0)
            if self.validate_word(word):
                return word
        print(f"Failed to find word: {self.wordle.current_word}")
        return False

    def score_word(self, word):
        score = 0
        for pos, letter in enumerate(word):
            score += self.stat_dict[pos].index(letter)
        return score

    def exclusive_words(self, wl=[], remainder=None, no_doubles=True):
        if remainder is None:
            remainder = self.remaining_words.copy()
        if len(remainder) > 0:
            for word in remainder:
                if not no_doubles or len(set(word)) == len(word):
                    new_remainder = list(
                        filter(
                            lambda x: set(x).intersection(set(word)) == set(), remainder
                        )
                    )
                    return self.exclusive_words(wl + [word], new_remainder)
        else:
            return wl

    def index_list_to_word(self, i_list):
        word = []
        for i in range(self.wordle.size):
            word.append(self.stat_dict[i][i_list[i]])
        return "".join(word)

    def validate_word(self, word):
        for x in self.letters_in_word:
            if x not in word:
                return False
        for pos in self.in_pos_letters:
            if word[pos] != self.in_pos_letters[pos]:
                return False
        for i, x in enumerate(word):
            if i not in self.possibilities_dict[x]:
                return False
        return self.wl_obj.contains(word)

    def print_info(self):
        if self.letters_in_word != []:
            for letter in self.letters_in_word:
                print(f"Letter: {letter}")
                print(",".join(self.possibilities_dict[letter]))
        else:
            print("No information")
