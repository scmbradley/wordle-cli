from word_list import WordList
from wordle import Wordle
from wordle_solver import WordleSolver

w = Wordle(base_word_list="multi.txt", verbose=False)

s = WordleSolver(wordle=w)

baseline = s.multisolver(100)
