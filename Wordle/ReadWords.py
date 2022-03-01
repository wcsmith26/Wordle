from torch import sort

def ReadWords():
    file = open("wordle-allowed-guesses.txt", "r")
    guesses = file.read().splitlines()
    file.close()

    file = open("wordle-answers-alphabetical.txt", "r")
    answers = file.read().splitlines()
    file.close()

    all_words = []
    for word in guesses:
        all_words.append(word)
    for word in answers:
        all_words.append(word)
        
    all_words.sort()
    return all_words, answers