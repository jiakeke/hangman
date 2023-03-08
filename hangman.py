#!/usr/bin/env python
# coding: utf-8

# # Hangman
# 
# ## Team Members:
# 
# - Aijun Fan
# - Dharshani Nuwanmali Rathnayake Rathnayake Mudhiyanselage
# - Ke Jia
# - Lakshitha Nisal Dharmarathna Kariyawasam Pathirage
# - Qixiao Zhang

# ### Project 5. Hangman
# 
# #### Requirements:
# 
# The game:
# 
# One player thinks a word and the other needs to guess it. Every time is a wrongly guessd letter, the other player will start to draw the hanged man picture. The player who is trying to guess, wins if the hanged man picture is not finalized.
# 
# The program should have the following options to choose from: friuts, animals, car brands, countries. Eeach category should contain at least 15 words to randomly choose from. The player should be abel to select the category and than game starts.
# 
# The program should allow user to play over and over again until user chooses to quit using it. When the game has stoped the program should display number of plays and numer of wins.
# 
# 35 points

# In[1]:


import random
import string


# ##### Here is the Hangman's picture with characters.

# In[2]:


HANGMAN_PICS = ["""
      +---+
      |
      |
      |
      |
      |
     ===""", """
      +---+
      |   O
      |
      |
      |
      |
     ===""", """
      +---+
      |   O
      |   |
      |
      |
      |
     ===""", """
      +---+
      |   O
      |  /|
      |
      |
      |
     ===""", """
      +---+
      |   O
      |  /|\ 
      |
      |
      |
     ===""", """
      +---+
      |   O
      |  /|\ 
      |  /
      |
      |
     ===""", """
      +---+
      |   O
      |  /|\ 
      |  / \ 
      |
      |
     ===""", """
      +---+
      |  (O
      |  /|\ 
      |  / \ 
      |
      |
     ===""", """
      +---+
      |  (O)
      |  /|\ 
      |  / \ 
      |
      |
     ===""", """
      +---+
      |   |
      |  (O)
      |  /|\ 
      |  / \ 
      |
     ==="""]


# ##### Here is the vocabulary for guessing.

# In[3]:


words = [
    ('Colors',
        ('red orange yellow green blue indigo violet white black brown')),
    ('Shapes',
        ('square triangle rectangle circle ellipse rhombus trapazoid chevron '
         'pentagon hexagon septagon octogon')),
    ('Fruits',
        ('apple orange lemon lime pear watermelon grape grapefruit cherry '
         'banana cantalope mango strawberry tomato')),
    ('Animals',
        ('bat bear beaver cat cougar crab deer dog donkey duck eagle fish frog '
         'goat leech lion lizard monkey moose mouse otter owl panda python '
         'rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale '
         'wolf wombat zebra'))
    ]

words_dict = dict([(k, v.split()) for k, v in words])


# ##### To clear previous screen for displaying the coming information.
# 
# It will support to run on:
# - Windows
# - Linux
# - Mac
# - Jupyter Notebook
# - ...

# In[4]:


def clear_screen():
    import os
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    import sys
    if 'ipykernel' in sys.modules:
        from IPython.display import clear_output
        clear_output()
    print('\n================ H A N G M A N ================\n')


# ##### To get a random word by category which user entered.

# In[5]:


def get_random_word(words_dict):
    keys = list(words_dict.keys())
    text = 'Enter category: '
    category = 0
    choices = ', '.join(['%s - %s' % (num+1, keys[num])for num in range(len(keys))])
    while category not in range(1, len(keys)+1):
        print(text, choices)
        category = int(input())
    word_category = keys[category-1]
    word = random.choice(words_dict[word_category])
    return [word, word_category]


# ##### To display game board
# - Display the category of the secret word
# - Display current Hangman picture
# - Display the missed letters
# - Display the secret word with spaces

# In[6]:


def display_board(missed_letters, correct_letters, secret_word):
    print('--------------------------')
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secret_word)

    for i in range(len(secret_word)): # replace blanks with correctly guessed letters
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    for letter in blanks: # show the secret word with spaces in between each letter
        print(letter, end=' ')
    print()


# ##### To get the guess letter entered by the user:
# - Only enter ONE guess LETTER each time
# - Re-enter a new one if user enters less/more than one letter
# - Re-enter a new one if user enters a letter has been guessed before
# - Re-enter a new one if user enters a non-letter charater
# 

# In[7]:


def get_guess(already_guessed):
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in string.ascii_lowercase:
            print('Please enter a LETTER.')
        else:
            return guess


# ##### This function returns True if the player wants to play again, otherwise it returns False.

# In[8]:


def play_again():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


# ##### To set the difficulty of the game. There are three levels in total.

# In[9]:


def set_difficulty():
    difficulty = 'X'
    while difficulty not in 'EMH':
      print('Enter difficulty: E - Easy, M - Medium, H - Hard')
      difficulty = input().upper()
    if difficulty == 'M':
        del HANGMAN_PICS[8]
        del HANGMAN_PICS[7]
    if difficulty == 'H':
        del HANGMAN_PICS[8]
        del HANGMAN_PICS[7]
        del HANGMAN_PICS[5]
        del HANGMAN_PICS[3]


# ##### The main execution function of the game:
# - Show game board
# - Run the guessing loop
# 

# In[10]:


def play():
    missed_letters = ''
    correct_letters = ''
    secret_word, secretSet = get_random_word(words_dict)

    while True:
        clear_screen()
        print('The secret word is in the set: ' + secretSet)
        display_board(missed_letters, correct_letters, secret_word)

        # Let the player type in a letter.
        guess = get_guess(missed_letters + correct_letters)

        if guess in secret_word:
            correct_letters += guess

            # Check if the player has won
            found_all_letters = True
            for item in secret_word:
                if item not in correct_letters:
                    found_all_letters = False
                    break
            if found_all_letters:
                print('Perfect! You get he secret word: "' + secret_word + '"! You win!')
                return 1
        else:
            missed_letters += guess

            # Check if player has guessed too many times and lost.
            if len(missed_letters) == len(HANGMAN_PICS) - 1:
                clear_screen()
                print('Unfortunately! You have run out of guesses!')
                display_board(missed_letters, correct_letters, secret_word)
                print(
                    'The word is "%s", you got %s times correctly and you missed %s.' % (
                        secret_word, len(correct_letters), len(missed_letters)))
                return 0


# In[11]:


if __name__ == "__main__":

    clear_screen()
    set_difficulty()
    tries = 0
    wins = 0
    first = True

    while first or play_again():
        first = False
        win = play()
        tries += 1
        wins += win

    print('You win %s out of %s games' % (wins, tries))

