from typing import Type
import Game
import ReadWords
import numpy


def CountAllLetterMatches(words):
    '''
    Takes in an array of all words to be considered.
    Returns a 3 by 5 array (freq) that contains the amount of times
    each letter appears as green, yellow, or red according to the
    Wordle rules.
    '''
    out = {}
    alphabet = []
    for i in range(26):
        num = ord('a') + i
        alphabet.append(chr(num))
    for letter in alphabet:
        green = [0,0,0,0,0]
        yellow = [0,0,0,0,0]
        red = [0,0,0,0,0]
        for word in words:
            for i in range(5):
                if (letter == word[i]):
                    green[i] += 1
                elif (letter not in word):
                    red[i] += 1
                else:
                    yellow[i] += 1
        out[letter] = [green, yellow, red]
    return out     

def CountGuessLetterMatches(guess, freq):
    '''
    Takes parameters guess (str) and freq (3x5 array) and finds the respective
    amount that each letter appears as green, yellow, or red in the index it appears
    according to the freq array.
    Returns a dictionary (out) that contains the amount of times each index matches 
    as green, yellow, and red in the current wordset.
    '''
    out = {0: [], 1: [], 2: [], 3: [], 4: []}
    for i in range(5):
        for j in range(3):
            out[i].append(freq[guess[i]][j][i])
    return out

def QuantifyGuess(freq):
    '''
    Given the frequency dictionary (freq) for a given guess, this method roughly
    quantifies a guess by awarding 2 points per green match and 1 point per yellow
    match.
    Returns an int (num) that represents how relatively good the guess is. 
    '''
    num = 0
    for j in range(3):
        for i in range(5):
            if (j == 0):
                num += 2*freq[i][j]
            elif (j == 1):
                num += freq[i][j]
    return num

def ConvertInfo(info):
    '''
    Takes an array of len=5 (info) and converts 'g' to 'green',
    'y' to 'yellow', and 'r' to 'red'. This is useful to print in
    tandem with the colored(str, color) method.
    Returns the converted array containing colors instead of chars.
    '''
    out = []
    for i in range(5):
        if (info[i] == 'g'):
            out.append('green')
        elif (info[i] == 'y'):
            out.append('yellow')
        elif (info[i] == 'r'):
            out.append('red')
    return out
            
def NarrowPool(guess, info, words):
    '''
    Takes a 5 char string (guess), a len=5 array (info), and the set of all words (words)
    and narrows the set of words down based upon the guess and info given. Use this method
    if you are playing without knowing the answer.
    Returns a smaller set of words, that has been narrowed down by the guess and info.
    '''
    new_words = []
    bad_letters = []
    for i in range(5):
        if (info[i] == 'r'):
            bad_letters.append(guess[i])
    for word in words:
        if (((info[0] == 'g' and guess[0] == word[0]) or (info[0] == 'y' and guess[0] in word and guess[0] != word[0]) or (info[0] == 'r' and word.count(guess[0]) != guess.count(guess[0]) and guess[0] not in word))
            and ((info[1] == 'g' and guess[1] == word[1]) or (info[1] == 'y' and guess[1] in word and guess[1] != word[1]) or (info[1] == 'r' and word.count(guess[1]) != guess.count(guess[1]) and guess[1] not in word))
            and ((info[2] == 'g' and guess[2] == word[2]) or (info[2] == 'y' and guess[2] in word and guess[2] != word[2]) or (info[2] == 'r' and word.count(guess[2]) != guess.count(guess[2]) and guess[2] not in word))
            and ((info[3] == 'g' and guess[3] == word[3]) or (info[3] == 'y' and guess[3] in word and guess[3] != word[3]) or (info[3] == 'r' and word.count(guess[3]) != guess.count(guess[3]) and guess[3] not in word))
            and ((info[4] == 'g' and guess[4] == word[4]) or (info[4] == 'y' and guess[4] in word and guess[4] != word[4]) or (info[4] == 'r' and word.count(guess[4]) != guess.count(guess[4]) and guess[4] not in word))):
            new_words.append(word)
    for word in new_words:
        for letter in bad_letters:
            if (letter in word and guess.count(letter) != word.count(letter)):
                new_words.remove(word)
                break
    return new_words   

def FillBins(guess, words):
    '''
    Currently not used, future implementation will utilize
    this to better play Wordle.
    Takes a guess (guess), and the set of words (words).
    Initializes and fills each possible information 
    outcome in a dictionary and fills the bins with the
    amount of words that would remain with the guess and
    corresponding info.
    Returns the dictionary created by this process.
    '''
    options = ['g', 'y', 'r']
    info = ['', '', '', '', '']
    data = {}

    for i in range(3):
        info[0] = options[i]
        for j in range(3):
            info[1] = options[j]
            for k in range(3):
                info[2] = options[k]
                for l in range(3):
                    info[3] = options[l]
                    for m in range(3):
                        info[4] = options[m]
                        key = info[0]+info[1]+info[2]+info[3]+info[4]
                        data[key] = (len(NarrowPool(guess, info, words)))
    return data
            
def MakeGuess(words):
    '''
    Takes the set of words.
    Returns the best guess, according to the algorithm.
    '''
    max_value = 0
    best_guess = ''
    freq = CountAllLetterMatches(words)
    for guess in words:
        guess_freq = CountGuessLetterMatches(guess, freq)
        check = True
        for i in range(5):
            if (guess.count(guess[i]) > 1):
                check = False
        if (check): 
            if (max_value <= QuantifyGuess(guess_freq)):
                max_value = QuantifyGuess(guess_freq)
                best_guess = guess
        else: 
            if (max_value <= QuantifyGuess(guess_freq) / 2):
                max_value = QuantifyGuess(guess_freq) / 2
                best_guess = guess
    return best_guess