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
        assert solver_cares.in_pos_letters[0] == "C"
        assert solver_cares.letters_in_word == set(["C", "R", "E", "A"])
        assert solver_cares.possibilities_dict["R"] == set([0, 1, 2, 3])
        assert solver_cares.possibilities_dict["Z"] == set([0, 1, 2, 3, 4])


class TestSolverScoreWord:
    def test_solver_score_cares(self, solver_cares):
        assert solver_cares.score_word("CARES") == 1


class TestSolverWordPicker:
    def test_index_list_to_word(self, solver_cares):
        assert solver_cares.index_list_to_word([0, 0, 0, 0, 0]) == "SARES"
        assert solver_cares.index_list_to_word([1, 1, 1, 1, 1]) == "COAAE"
        assert solver_cares.pick_word() == "SAREE"


class TestValidateWord:
    def test_validate_initial(self, solver_cares):
        assert solver_cares.validate_word("CARES")
        assert not solver_cares.validate_word("BZZZZ")

    def test_validate_after_guess(self, solver_cares, wordle_cares):
        g = wordle_cares.guess("TUFTS")
        solver_cares.parse_report(g)
        assert solver_cares.validate_word("CARES")
        assert not solver_cares.validate_word("BZZZZ")


class TestSolverSolve:
    def test_solver_solves(self, solver_cares):
        solver_cares.solve()
        assert solver_cares.wordle.solved

    def test_solver_handles_double_letter(self):
        w = Wordle()
        w.new_game(word="LOOPY")
        s = WordleSolver(w)
        s.solve()
        assert s.wordle.solved

    def test_solver_resets(self, solver_cares):
        solver_cares.solve()
        solver_cares.new_game()
        assert solver_cares.wordle.solved is False
        solver_cares.solve()
        assert solver_cares.wordle.solved
