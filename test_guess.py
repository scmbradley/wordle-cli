import pytest
from wordle import Wordle, GuessStatus
from wordle_solver import WordleSolver


@pytest.fixture
def wordle_cares():
    w = Wordle()
    w.new_game(word="CARES")
    return w


@pytest.fixture
def solver_cares(wordle_cares):
    return WordleSolver(wordle_cares)


@pytest.fixture
def guess_cares_clear(wordle_cares):
    return wordle_cares.guess("CLEAR")


class TestGuess:
    def test_guess_win(self, wordle_cares):
        g = wordle_cares.guess("CARES")
        assert g.winner() is True

    def test_guess_one_hit(self, wordle_cares):
        g = wordle_cares.guess("TUFTS")
        assert g.report[4][1] == GuessStatus.IN_POS
        for i in range(4):
            assert g.report[i][1] == GuessStatus.WRONG


class TestGuessFormatter:
    def test_formatter(self, wordle_cares):
        assert wordle_cares.formatter(GuessStatus.IN_POS) == "X"
        assert wordle_cares.formatter(GuessStatus.IN_WORD) == "/"
        assert wordle_cares.formatter(GuessStatus.WRONG) == " "


class TestSolverBasics:
    def test_parse_report(self, solver_cares, guess_cares_clear):
        solver_cares.parse_report(guess_cares_clear)
        assert solver_cares.info_dict["C"] == set([0])
        assert solver_cares.letters_in_word == set(["C", "R", "E", "A"])
        assert solver_cares.info_dict["R"] == set([0, 1, 2, 3])
        assert solver_cares.info_dict["Z"] == set([0, 1, 2, 3, 4])
