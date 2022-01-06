from collections import Counter
from pathlib import Path
import re


strip_punctuation = re.compile(r'[,.!?"_;:-]')


def gen_word_list(filename_in, filename_out, max_words=10_000):
    word_counter = Counter()
    with Path(filename_in).open() as data:
        for line in data:
            words = strip_punctuation.sub("", line).strip().upper().split()
            words = [x for x in words if "'" not in x]
            word_counter.update(words)

    word_list = "\n".join([x[0] for x in word_counter.most_common(max_words)])

    file_out = Path(filename_out)

    file_out.write_text(word_list)


def top_letters(ctr, top_n=10):
    return ",".join([x[0].upper() for x in ctr.most_common(top_n)])


def word_list_stats(word_list, num=None, top_n=10):
    with open(word_list) as d:
        wl = [x.strip() for x in d.readlines()]

    if num is not None:
        print(f"Restricting corpus to {num} letter words")

    print("The most common letters in any position")
    print(top_letters(Counter("".join(wl)), top_n=top_n))

    if num is not None:
        n_letter_words = [x for x in wl if len(x) == num]
        for i in range(num):
            print(f"Top letters in position {i+1}")
            letters = [x[i] for x in n_letter_words]
            print(top_letters(Counter(letters), top_n=top_n))
