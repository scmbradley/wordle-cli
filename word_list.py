from collections import Counter
from pathlib import Path
import re
import random


class WordList:
    @staticmethod
    def generate(filename_in, filename_out, max_words=10_000):
        word_counter = Counter()
        strip_punctuation = re.compile(r"(\W|_)")
        with Path(filename_in).open() as data:
            for line in data:
                words = [
                    x
                    for x in line.strip().upper().split()
                    if not WordList.is_contraction(x)
                ]
                word_counter.update([strip_punctuation.sub("", x) for x in words])
        word_list = [x[0] for x in word_counter.most_common(max_words)]
        file_out = Path(filename_out)
        file_out.write_text("\n".join(word_list))
        print(f"Wrote out to file {filename_out}")
        return WordList(filename_out)

    def __init__(self, filename, alphabetise=False):
        with open(filename) as data:
            self.word_list = [x.strip() for x in data.readlines()]
        if alphabetise:
            self.word_list.sort()
        self.filename = filename

    @staticmethod
    def is_contraction(word):
        return "'" in word[1:-1] or "’" in word[1:-1]

    def contains(self, word):
        return word in self.word_list

    def wl_alpha(self):
        return sorted(self.word_list)

    def top_letters(self, ctr, top_n=10):
        return [x[0].upper() for x in ctr.most_common(top_n)]

    def most_common_letters(self):
        return self.position_stats(top_n=26)["total"]

    def n_letter_words(self, n):
        return [x for x in self.word_list if len(x) == n]

    def write_n_letter_list(self, n):
        p = Path(self.filename)
        filename_out = Path(p.stem + "_" + str(n) + p.suffix)
        filename_out.write_text("\n".join(self.n_letter_words(n)))

    def pick_random(self):
        return random.choice(self.word_list)

    def position_stats(self, num=None, top_n=26):
        pos_stats = dict()
        words_to_count = []
        if num is not None:
            words_to_count = self.n_letter_words(num)
        else:
            words_to_count = self.word_list

        pos_stats["total"] = self.top_letters(
            Counter("".join(words_to_count)), top_n=top_n
        )
        if num is not None:
            for i in range(num):
                letters = [x[i] for x in words_to_count]
                pos_stats[i] = self.top_letters(Counter(letters), top_n=top_n)
        return pos_stats

    def print_stat_report(self, num=None, top_n=10):
        d = self.position_stats(num=num, top_n=top_n)
        if num is not None:
            print(f"Restricting corpus to {num} letter words")
        print(f"Top letters, all positions:")
        print(",".join(d["total"]))
        if num is not None:
            for i in range(num):
                print(f"Top letters in position {i+1}")
                print(",".join(d[i]))
