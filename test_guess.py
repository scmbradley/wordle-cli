import pytest
from wordle import Wordle, GuessStatus


@pytest.fixture
def wordle_cares():
    w = Wordle()
    w.new_game(word="CARES")
    return w


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
    def test_formatter_in_pos(self, wordle_cares):
        assert wordle_cares.formatter(GuessStatus.IN_POS) == "X"

    def test_formatter_in_word(self, wordle_cares):
        assert wordle_cares.formatter(GuessStatus.IN_WORD) == "/"

    def test_formatter_wrong(self, wordle_cares):
        assert wordle_cares.formatter(GuessStatus.WRONG) == " "
