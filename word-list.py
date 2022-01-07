from collections import Counter
from pathlib import Path
import re


class WordList:
    def __init__(self, filename_in, max_words=10_000):
        word_counter = Counter()
        self.strip_punctuation = re.compile(r"(\W|_)")
        with Path(filename_in).open() as data:
            for line in data:
                words = [
                    x
                    for x in line.strip().upper().split()
                    if not self.is_contraction(x)
                ]
                words = self.strip_punctuation.sub("", line).strip().upper().split()
                words = [x for x in words if "'" not in x]
                word_counter.update(words)
        self.word_counter = word_counter
        self.word_list = [x[0] for x in word_counter.most_common(max_words)]

    def write_out(self, filename_out):
        file_out = Path(filename_out)
        file_out.write_text("\n".join(self.word_list))
        print(f"Wrote out to file {filename_out}")

    def is_contraction(self, word):
        return "'" in word[1:-1] or "’" in word[1:-1]

    def top_letters(self, ctr, top_n=10):
        return [x[0].upper() for x in ctr.most_common(top_n)]

    def n_letter_words(self, n):
        return [x for x in self.word_list if len(x) == n]

    def position_stats(self, num=None, top_n=10):
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
