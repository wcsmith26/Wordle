from asyncio.windows_events import NULL
from xmlrpc.client import Boolean, boolean
from torch import sort
from ReadWords import ReadWords
from termcolor import colored
from WordleAI import ConvertInfo, NarrowPool, MakeGuess
import random as rand

class Game:
    '''
    A class that represents a Wordle game.
    '''
    
    info = []
    
    def __init__(self, answer: str, unknown: bool = False, random: bool = True):
        '''
        Initializes a game object given an answer string that represents the answer,
        an unknown bool that represents whether or not the answer is unknown, and a
        random bool that represents if a random answer is desired or not.
        '''
        self.words, self.answers = ReadWords()
        self.random = random
        self.answer_unknown = unknown
        self.answer = answer
        if (self.answer_unknown == True):
            self.answer = ''
        elif (self.random == True):
            self.answer = rand.choice(self.answers)
        self.guesses = 6
    
    def GetInfo(cls):
        '''
        A method that when called prompts the user for the info
        array provided from the game.
        Return the info, that the user input.
        '''
        cls.info = input("Input info received from the guess: ")
        while (len(cls.info) != 5): 
            cls.info = input("Error, input info received from the guess: ")
        cls.info = [char for char in cls.info]
        return cls.info
            
    def TryGuess(cls, word):
        '''
        Takes a word to guess (word), and tries the guess. Depending on
        if the game is in the answer unknown state or answer known state,
        the method will then prompt the user for more information. 
        '''
        if (cls.guesses == 6):
            new_words = cls.words
        if (cls.answer_unknown):
            while (word not in cls.words):
                word = input("{} is not in the dataset, guess a new word: ".format(word))
            cls.guesses -= 1
            cls.info = cls.GetInfo()
            info = ConvertInfo(cls.info)
            for i in range(5):
                print(colored(word[i], info[i]), end='')
            print("")
            new_words = NarrowPool(word, cls.info, new_words)
            
            if (cls.info == ['g','g','g','g','g']):
                print("Congratulations you got the word in {} guesses!".format(6-cls.guesses))
                exit()
                
        else:
            while (len(word) != len(cls.answer)):
                word = input("The answer is {} letters long. Submit a new guess: ".format(len(cls.answer)))
            while (word not in cls.words):
                word = input("{} is not in the dataset, guess a new word: ".format(word))
            cls.guesses -= 1
            if (word == cls.answer):
                print(colored(word, 'green'))
                print("Congratulations you got the word in {} guesses!".format(6-cls.guesses))
                exit()
            for i in range(len(cls.answer)):
                if (word[i] == cls.answer[i]):
                    print(colored(word[i], 'green'), end='')
                elif (word[i] not in cls.answer):
                    print(colored(word[i], 'red'), end='')
                elif (word[i] in cls.answer and word[i] != cls.answer[i]):
                    print(colored(word[i], 'yellow'), end='')
            if (cls.guesses == 0):
                print("\nUnlucky! The word was {}!".format(cls.answer))
                exit()
    
    def CompareGuess(cls, guess):
        '''
        A method that takes a guess, and compares it when
        the answer is known.
        Returns an info array that is derived from the guess
        compared to the known answer.
        '''
        info = ['','','','','']
        for i in range(len(cls.answer)):
                if (guess[i] == cls.answer[i]):
                    info[i] = 'g'
                elif (guess[i] not in cls.answer):
                    info[i] = 'r'
                elif (guess[i] in cls.answer and guess[i] != cls.answer[i]):
                    info[i] = 'y'
        return info
            
    def Begin(cls):
        '''
        Begins the game.
        '''
        for i in range(1,7):
            guess = input("\nGuess {}: ".format(i))
            cls.TryGuess(guess)

    # ITERATION 1 SCORE = [1, 211, 2253, 4549, 3049, 1455, 1454]     
    def BeginAI(cls):
        '''
        A method that begins the game with an AI player,
        rather than a human player. The method prints the
        AI's guesses as it plays.
        '''
        new_words = cls.words
        for i in range(1,7):
            guess = MakeGuess(new_words)
            info = cls.CompareGuess(guess)
            print("\n")
            for j in range(5):
                colors = ConvertInfo(info)
                print(colored(guess[j], colors[j]), end='')
            print("\n")
            if (info == ['g','g','g','g','g']):
                print("The AI guessed the word in {} guesses!".format(i))
                return i
            old_len = len(new_words)
            new_words = NarrowPool(guess, info, new_words)
            new_len = len(new_words)
            print("Printing new words: {}".format(new_words))
            print("The guess {} narrowed the word pool down from {} words to {}".format(guess, old_len, new_len))
        print("The AI failed to guess the word.\nThe word was {}".format(cls.answer))
        return 7