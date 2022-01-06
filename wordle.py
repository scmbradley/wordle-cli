#! /usr/bin/python3

from collections import Counter
from pathlib import Path
import random
from enum import Enum, auto

with open("wordlist.txt") as d:
    word_list = [x.strip() for x in d.readlines()]


class Wordle:
    def __init__(self, size=5, base_word_list="wordlist.txt"):
        self.size = size
        bwl = Path(base_word_list)
        maybe_file = Path(bwl.stem + "_" + str(size) + bwl.suffix)
        if maybe_file.is_file():
            with maybe_file.open() as data:
                self.word_list = [x.strip() for x in data.readlines()]
        else:
            with bwl.open() as data:
                full_word_list = [x.strip() for x in data.readlines()]
                self.word_list = [x for x in full_word_list if len(x) == size]
                maybe_file.write_text("\n".join(self.word_list))
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
        if word is None:
            self.current_word = random.choice(self.word_list).upper()
        else:
            self.current_word = word
        print("OK, here we go.")

    def guess(self, w):
        word = w.upper()
        gr = GuessReport(self.current_word, word, self.formatter)
        if gr.winner():
            print("Winner winner")
        self.report_list.append(gr)
        return gr

    def formatter(self, x):
        d = {GuessStatus.WRONG: " ", GuessStatus.IN_POS: "X", GuessStatus.IN_WORD: "/"}
        return d[x]

    def ordered_letter_list(self):
        return "".join(
            [x[0] for x in Counter("".join(self.word_list)).most_common()]
        ).upper()

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
            elif len(x) == 5:
                g = self.guess(x)
                print(g)
                ct = not g.winner()
            else:
                print(
                    "Please type a five letter word or a command.\nType !help to see commands."
                )

    def unused_letters(self):
        letters = set("QWERTYUIOPASDFGHJKLZXCVBNM")
        for r in self.report_list:
            letters = letters.difference(r.letters())
        ret = ",".join(sorted(list(letters), key=self.ordered_letter_list().index))
        return ret


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
        return line_one + "\n" + line_two + "\n"


if __name__ == "__main__":
    w = Wordle()
    w.new_game()
    w.guess_interactive()
