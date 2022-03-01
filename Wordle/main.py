from Game import Game
from WordleAI import CountAllLetterMatches, CountGuessLetterMatches, MakeGuess, NarrowPool, FillBins

### Code used to test Iteration 1 of the AI
# wordbank = Game('')
# score = [0,0,0,0,0,0,0]

# for word in wordbank.words:
#     game = Game(word, unknown = False, random=False)
#     score[game.BeginAI()-1] += 1
# print(score)

### Code used to play Squabble.me an online game that involves Wordle
### To use, change the guess and info strings as you guess.
### RATES HOUND CLIMB THEORY
### Three words that I commonly use are rates, hound, and climb
### These words cover 15 different letters and the pool of words
### is very small after guessing these 3 words. In fact, the 
### largest pool of words is 34 words, where eases is the answer.
game = Game('', unknown=False, random=False)
new_words = NarrowPool('rates', 'rrrrr', game.words)
new_words = NarrowPool('hound', 'rrrrr', new_words)
new_words = NarrowPool('climb', 'rrrrr', new_words)
print(len(new_words))
print(new_words)