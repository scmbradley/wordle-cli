#! /usr/bin/python3

import wordle

w = wordle.Wordle(base_word_list="shakespeare.txt", size=5)
w.guess_interactive()
