#! /usr/bin/python3

import wordle

if __name__ == "__main__":
    w = wordle.Wordle(base_word_list="shakespeare.txt", size=6)
    w.guess_interactive()
