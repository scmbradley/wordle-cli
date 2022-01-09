#! /usr/bin/python3

from collections import Counter
from pathlib import Path
from enum import Enum, auto
from word_list import WordList


class Wordle:
    def __init__(
        self, size=5, base_word_list="wordlist.txt", only_words=True, verbose=True
    ):
        self.size = size
        self.only_words = only_words
        if verbose:
            self.print = print
        else:
            self.print = lambda x: None
        bwl = Path(base_word_list)
        maybe_file = Path(bwl.stem + "_" + str(size) + bwl.suffix)
        if maybe_file.is_file():
            self.word_list = WordList(maybe_file)
        else:
            big_list = WordList(bwl)
            big_list.write_n_letter_list(size)
            self.word_list = WordList(maybe_file)
        _help_list = [
            "!help: display this text.",
            "!quit: quit the game.",
            "!cheat: display the word.",
            "!letters: display unused letters (from most common to least).",
        ]
        self.help_text = "\n".join(_help_list)
        self.new_game()

    def new_game(self, word=None):
        self.report_list = []
        self.solved = False
        if word is None:
            self.current_word = self.word_list.pick_random()
        else:
            self.current_word = word
        self.print("New game.")

    def guess(self, w):
        word = w.upper()
        if self.only_words and not self.word_list.contains(word):
            self.print(f"{word} is not a word.")
            return InvalidGuessReport()
        gr = GuessReport(self.current_word, word, self.formatter)
        self.report_list.append(gr)
        if gr.winner():
            self.solved = True
            self.print(f"You guessed correctly in {len(self.report_list)} guesses.")
        return gr

    def formatter(self, x):
        d = {GuessStatus.WRONG: " ", GuessStatus.IN_POS: "X", GuessStatus.IN_WORD: "/"}
        return d[x]

    def cheat(self):
        self.print(self.current_word)

    def guess_interactive(self):
        ct = True
        while ct:
            x = input("guess> ")
            if x == "!quit":
                ct = False
            elif x == "!cheat":
                self.cheat()
            elif x == "!letters":
                self.print(self.unused_letters())
            elif x == "!help":
                self.print(self.help_text)
            elif len(x) == self.size:
                g = self.guess(x)
                self.print(g)
                ct = not g.winner()
            else:
                self.print(
                    f"Please type a {self.size} letter word or a command.\nType !help to see commands."
                )

    def unused_letters(self):
        letters = set("QWERTYUIOPASDFGHJKLZXCVBNM")
        for r in self.report_list:
            letters = letters.difference(r.letters())
        ret = ",".join(
            sorted(list(letters), key=self.word_list.most_common_letters().index)
        )
        return ret

    def show_stats(self):
        self.word_list.print_stat_report(num=self.size)

    def guessed_words(self):
        return [x.guess for x in self.report_list]

    def num_guesses(self):
        return len(self.report_list)


class GuessStatus(Enum):
    WRONG = auto()
    IN_WORD = auto()
    IN_POS = auto()


class GuessReport:
    def __init__(self, word, guess, formatter):
        self.report = []
        self.formatter = formatter
        self.guess = guess
        for i, x in enumerate(guess):
            if x == word[i]:
                self.report.append((x, GuessStatus.IN_POS))
            elif x in word:
                self.report.append((x, GuessStatus.IN_WORD))
            else:
                self.report.append((x, GuessStatus.WRONG))

    def winner(self):
        return set([x[1] for x in self.report]) == {GuessStatus.IN_POS}

    def letters(self):
        return set([x[0] for x in self.report])

    def correct_letters(self):
        return set([x[0] for x in self.report if x[1] != GuessStatus.WRONG])

    def __repr__(self):
        line_one = " ".join([x[0] for x in self.report])
        line_two = " ".join(self.formatter(x[1]) for x in self.report)
        return line_one + "\n" + line_two


class InvalidGuessReport(GuessReport):
    def __init__(self):
        pass

    def __repr__(self):
        return ""

    def winner(self):
        return False
