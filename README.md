# Wordle-CLI
A command line version of [Wordle](https://www.powerlanguage.co.uk/wordle/).

Here's a sample session of the game.

```
me@mypc: ./play_wordle.py 
New game.
guess> cares
C A R E S
      / X
guess> !letters
T,O,L,I,N,D,H,U,P,G,B,M,W,Y,F,K,V,J,Q,X,Z
guess> toils
T O I L S
X     X X
guess> tells
You guessed correctly in 3 guesses.
T E L L S
X X X X X
```
The best way to change options is to edit `play_wordle.py` directly.
There are five word lists included.

 - `shakespeare.txt`: extracted from the 
   [Complete Works of Shakespeare](https://www.gutenberg.org/files/100/100-0.txt).
   Specifically, it's the 10,000 most used words in that text file.

 - `winnie.txt`: extracted from 
   [Winnie the Pooh](https://www.gutenberg.org/cache/epub/67098/pg67098.txt).
   This is all 2400 ish words used in that book.

 - `wiki.txt`: extracted using the `WordList.wiki_corpus` method.
   This is a list of words that appear in 1000 random wikipedia articles.
   This could contain some proper names, or some foreign words,
   it depends on which articles it retrieves.
   
 - `multi.txt`: the top 15,000 words of the above three lists combined.
   This is probably the most sensible list to use.
   It contains about 2100 five letter words.

 - `wordlist.txt`: a truly mammoth 
   [word list](https://github.com/dwyl/english-words).
   There are 370,000 words listed here. 
   Although there appear to be some typos in there.

There is also a
set of tools for taking any text file and generating
a list of most common words for use as a base word list for
wordling.
Use `WordList.generate` to create a new word list from any input text file.

