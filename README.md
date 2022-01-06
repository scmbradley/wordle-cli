# Wordle-CLI
A command line version of [Wordle](https://www.powerlanguage.co.uk/wordle/).

Here's a sample session of the game.

```
OK, here we go.
guess> cares
C A R E S
         
guess> bound
B O U N D
        /
guess> !letters
I,L,T,Y,M,P,H,G,K,F,W,V,Z,J,X,Q
guess> tiled
T I L E D
/ X     /
guess> !cheat
DIGIT
guess> digit
Winner winner
D I G I T
X X X X X
```

You can just `chmod +X wordle.py` and then run `./wordle.py`,
but currently that means only using the default options.
You probably don't want to do this since the default uses an
absolutely massive list of words, and thus you'll probably get a
really obscure word like `OBELI` or `SEQED`.
See `sample-game-run.py` for a way to run the game with options set.

There is also a -- currently undocumented --
set of crude tools for taking any text file and generating
a list of most common words for use as a base word list for
wordling.


