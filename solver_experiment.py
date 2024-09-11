from word_list import WordList
from wordle import Wordle
from wordle_solver import WordleSolver
from scipy.stats import describe

import matplotlib.pyplot as plt


def print_result_stats(solver_output):
    values = [x[0] for x in solver_output]
    d = describe(values)
    print(f"Mean: {d.mean:.2}, Variance: {d.variance:.2}, Min/Max: {d.minmax}")


# Here we go:

w = Wordle(base_word_list="multi.txt", verbose=False)

s = WordleSolver(wordle=w)

ew = s.exclusive_words(permit_doubles=True)

NUM_SOLVES = 8192

print("Exclusive words: " + ",".join(ew))

print("Baseline stats:")

baseline = s.multisolver(NUM_SOLVES)

print_result_stats(baseline)

print("Do two words first:")

two_words = s.multisolver(NUM_SOLVES, firsts=ew[:2])

print_result_stats(two_words)

print("Do three words first:")

three_words = s.multisolver(NUM_SOLVES, firsts=ew)

print_result_stats(three_words)

# alt_res = s.multisolver(NUM_SOLVES, firsts=alt)

# print_result_stats(alt_res)

baseline_values = [x[0] for x in baseline]
two_values = [x[0] for x in two_words]
three_values = [x[0] for x in three_words]
plt.close("all")
plt.hist(
    [baseline_values, two_values, three_values],
    bins,
    label=["baseline", "two words", "three words"],
)
plt.legend(loc="upper right")
plt.savefig("experiment1.png")
