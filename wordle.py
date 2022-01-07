#! /usr/bin/python3

from collections import Counter
from pathlib import Path
from enum import Enum, auto
from word_list import WordList


class Wordle:
    def __init__(self, size=5, base_word_list="wordlist.txt"):
        self.size = size
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
        print("New game.")

    def guess(self, w):
        word = w.upper()
        gr = GuessReport(self.current_word, word, self.formatter)
        self.report_list.append(gr)
        if gr.winner():
            self.solved = True
            print(f"You guessed correctly in {len(self.report_list)} guesses.")
        return gr

    def formatter(self, x):
        d = {GuessStatus.WRONG: " ", GuessStatus.IN_POS: "X", GuessStatus.IN_WORD: "/"}
        return d[x]

    def cheat(self):
        print(self.current_word)

    def guess_interactive(self):
        ct = True
        while ct:
            x = input("guess> ")
            if x == "!quit":
                ct = False
            elif x == "!cheat":
                self.cheat()
            elif x == "!letters":
                print(self.unused_letters())
            elif x == "!help":
                print(self.help_text)
            elif len(x) == self.size:
                g = self.guess(x)
                print(g)
                ct = not g.winner()
            else:
                print(
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


class GuessStatus(Enum):
    WRONG = auto()
    IN_WORD = auto()
    IN_POS = auto()


class GuessReport:
    def __init__(self, word, guess, formatter):
        self.report = []
        self.formatter = formatter
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

    def __repr__(self):
        line_one = " ".join([x[0] for x in self.report])
        line_two = " ".join(self.formatter(x[1]) for x in self.report)
        return line_one + "\n" + line_two
