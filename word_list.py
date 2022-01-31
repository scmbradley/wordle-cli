from collections import Counter
from pathlib import Path
import re
import random
import wikipedia


class WordList:
    @staticmethod
    def generate(filename_in, filename_out, max_words=10_000, word_length=None):
        word_counter = Counter()
        strip_punctuation = re.compile(r"(\W|_|\d)")
        with Path(filename_in).open() as data:
            for line in data:
                words = [
                    x
                    for x in line.strip().upper().split()
                    if not WordList.is_contraction(x)
                ]
                word_counter.update([strip_punctuation.sub("", x) for x in words])
        if word_length is None:
            word_list = [x[0] for x in word_counter.most_common(max_words)]
        else:
            n_word_list = [
                x[0] for x in word_counter.most_common() if len(x[0]) == word_length
            ]
            if len(n_word_list) < max_words:
                word_list = n_word_list
            else:
                word_list = n_word_list[:max_words]
        file_out = Path(filename_out)
        file_out.write_text("\n".join(word_list))
        print(f"Wrote out to file {filename_out}")
        return WordList(filename_out)

    @staticmethod
    def wiki_corpus(
        filename_raw=None, filename_out="wiki.txt", num_pages=100, **kwargs
    ):
        if filename_raw is None:
            _filename = Path("wiki_tmp.txt")
        else:
            _filename = Path(filename_out)
        wiki_page_list = wikipedia.random(pages=num_pages)
        wiki_contents = ""
        pages_done = 0
        for page in wiki_page_list:
            try:
                wiki_contents += wikipedia.page(page, auto_suggest=False).content
            except wikipedia.DisambiguationError as err:
                try:
                    wiki_contents += wikipedia.page(
                        err.options[0], auto_suggest=False
                    ).content
                except:
                    pages_done -= 1
                    print("Uncaught error. Sad face.")
            pages_done += 1
            if pages_done % 5 == 0:
                print(f"Pages done: {pages_done}")
        _filename.write_text(wiki_contents)
        wl = WordList.generate(_filename, filename_out, **kwargs)
        if filename_raw is None:
            _filename.unlink()
        return wl

    def __init__(self, filename, alphabetise=False):
        with open(filename) as data:
            word_list = [x.strip() for x in data.readlines()]
        if alphabetise:
            self.word_list = sorted(word_list)
        else:
            self.word_list = set(word_list)
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
        return random.choice(tuple(self.word_list))

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
