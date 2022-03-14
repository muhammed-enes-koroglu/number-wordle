from calendar import c
import getpass
import random
from typing import Set, Tuple

from numpy import character

BASE_10_SET: Set[str] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
BASE_16_SET: Set[str] = set.union(BASE_10_SET, {'a', 'b', 'c', 'd', 'e', 'f'})


# Returns `(secret_code, base)`.
def get_secret_code() -> Tuple[str, int]:

    # Get the base.
    base: int = int(input('Which base? (10 or 16): '))
    if(base != 10 and base != 16):
        raise ValueError('Base should be either 10 or 16! It is: ' + str(base))
    
    secret_code:str = getpass.getpass('Enter the secret code, or type `r` or `random` if you want a random secret code: ')
    # Handle random secret code.
    if(secret_code == 'r' or secret_code == 'random'):
        return (get_random_secret_code(base), base)
    
    # Check if the given code conforms the given base.
    if(base == 10):
        if(any(elm not in BASE_10_SET for elm in secret_code)):
            raise ValueError('Given secret code is not in base 10!: ' + secret_code)
        if(string_contains_repeating_element(secret_code)):
            raise ValueError('Given secret code contains repeating elements!: ' + secret_code)
    else:
        if(any(elm not in BASE_16_SET for elm in secret_code)):
            raise ValueError('Given secret code is not in base 16!: ' + secret_code)
        if(string_contains_repeating_element(secret_code)):
            raise ValueError('Given secret code contains repeating elements!: ' + secret_code)
    
    return (secret_code, base)


# Returns a secret code in the given base.
def get_random_secret_code(base: int) -> str:
    nb_digits: int = int(input('How many digits do you want? (3-5 recommended): '))
    secret_code: str = ''
    available_char_set:Set[str]

    if(base == 10): # Determine which set to use.
        available_char_set = BASE_10_SET.copy()
    else:
        available_char_set = BASE_16_SET.copy()

    while(nb_digits > 0):
        random_char: str = random.choice(list(available_char_set))
        available_char_set.remove(random_char)  # Remove used char from list so no character repeats.
        secret_code += random_char

        nb_digits -= 1

    return secret_code


# Gives feedback of the from '+1 -2' on a given guess.
def feedback_on_guess(guess: str) -> str:
    nb_correct_placed: int = 0
    nb_wrong_placed: int = 0
    
    index: int
    for index in range(len(guess)):
        elm: str = guess[index]
        if(elm in secret_code):
            if(secret_code[index] == elm):
                nb_correct_placed += 1
            else:
                nb_wrong_placed += 1
    
    return '+' + str(nb_correct_placed) + ' -' + str(nb_wrong_placed)


def string_contains_repeating_element(string:str) -> bool:
    return any(string.count(elm) > 1 for elm in string)


if __name__ == "__main__":
    result: tuple = get_secret_code()
    secret_code: str = result[0]
    base: int = result[1]

    # The game loop.
    guess: str = ''
    feedback: str = ''
    nb_tries: int = 0
    while(guess != 'quit'):
        
        # Let the player make a guess.
        guess_prompt: str = 'Take a guess: '
        guess = input(guess_prompt)
        # Check if player gave up.
        if(guess == 'quit'):
            continue
        
        # Check if the guess is conform the rules.
        if(len(guess) != len(secret_code)):
            print('Your guess should match the length of the secret code, which is ', len(secret_code))
            continue
        if(string_contains_repeating_element(guess)):
            print('Your guess may not contain repeating characters!')
            continue

        nb_tries += 1        
        feedback = feedback_on_guess(guess)
        # Check if player won. Else give feedback.
        if(feedback.count('+' + str(len(secret_code)))):
            print('Congrats!! You guessed correctly!')
            print('Number of tries: ' + str(nb_tries))
            break
        else:
            print(' ' * (len(guess_prompt) + len(guess) + 1) + feedback)

        


