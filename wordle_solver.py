from wordle import Wordle, GuessStatus


class WordleSolver:
    def __init__(self, wordle=None, wl_obj=None):
        if wordle is None:
            self.wordle = Wordle(verbose=False)
        else:
            self.wordle = wordle
        if wl_obj is None:
            self.wl_obj = self.wordle.word_list
        self.stat_dict = self.wl_obj.position_stats(num=self.wordle.size)
        self.words_score_order = sorted(self.wl_obj.word_list, key=self.score_word)
        self.reset_for_new_game()

    def reset_for_new_game(self):
        self.possibilities_dict = dict()
        for letter in "QWERTYUIOPASDFGHJKLZXCVBNM":
            self.possibilities_dict[letter] = set(range(self.wordle.size))
        self.letters_in_word = set()
        self.in_pos_letters = dict()
        self.remaining_words = self.words_score_order.copy()

    def new_game(self, **kwargs):
        self.reset_for_new_game()
        self.wordle.new_game(**kwargs)

    def guess(self, word):
        r = self.wordle.guess(word)
        self.parse_report(r)

    def solve(self, first_guesses=[]):
        for guess in first_guesses:
            self.guess(guess)
            if self.wordle.solved:
                return True
        while self.wordle.solved is False:
            word = self.pick_word()
            self.guess(word)

    def parse_report(self, report):
        self.letters_in_word.update(report.correct_letters())
        for pos, letter_report in enumerate(report.report):
            letter, status = letter_report
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

        return wl

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

    def multisolver(self, num_games=10, firsts=[]):
        results = []
        for i in range(num_games):
            self.new_game()
            self.solve(first_guesses=firsts)
            results.append((self.wordle.num_guesses(), self.wordle.current_word))
        return results

    def multisolver_stats(self, num_games=10, firsts=[]):
        output = self.multisolver(num_games=num_games, firsts=firsts)
        values = [x[0] for x in output]
        print(f"min: {min(values)}, max: {max(values)}, avg: {sum(values)/len(values)}")
