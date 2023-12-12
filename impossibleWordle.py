import random
import re
import os

def search_words_with_letters(file_path, letters):
    filtered_words = []
    
    with open(file_path, 'r') as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line)
            
            filtered_words.extend([word for word in words if any(letter in word for letter in letters)])

    return filtered_words

def generate_word(current_word, user_guessed_letters, words):
    while True:
        possible_words = search_words_with_letters("words.txt", user_guessed_letters)

        if possible_words:
            new_word = random.choice(possible_words)
            if set(new_word) != set(current_word):
                break
        else:
            new_word = random.choice(words)
            if set(new_word) != set(current_word):
                break

    return new_word


def display_word(word, guessed_words):
    display = ""
    for letter in word:
        if letter in guessed_words:
            display += letter
        else:
            display += "-"
    return display

def modify_word(word, guessed_letters, words):
    possible_words = [w for w in words if all(letter in w for letter in guessed_letters) and w != word]

    return random.choice(possible_words) if possible_words else generate_word(word, guessed_letters, words)





def is_valid_word(word):
    return len(word) == 5 and word.isalpha()

def play_wordle(words):
    max_attempts = 6
    guessed_letters = set()

    while True:
        word_to_guess = generate_word("", guessed_letters, words)

        print("Welcome to Impossible Wordle.")
        print("Good luck! :D")

        for attempt in range(1, max_attempts + 1):
            print("\nAttempt", attempt)

            guess = input("Enter a word: ").lower()

            if not is_valid_word(guess):
                print("Invalid input. Please enter a 5-letter word.")
                continue

            correct_letters = set(letter for letter in guess if letter in word_to_guess)

            if correct_letters:
                guessed_letters.update(correct_letters)

                feedback = "\n" + "\n".join(f"{letter} is in the word." for letter in correct_letters)
                print(feedback)

                if guessed_letters == set(word_to_guess):
                    print("\nCongratulations! You guessed the word:", word_to_guess)
                    break
            else:
                print("No letters in the word.")
                word_to_guess = modify_word(word_to_guess, guessed_letters, words)
        else:
            print("\nYou have run out of attempts. The word was:", word_to_guess)

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_directory, "words.txt")

    with open(file_path, "r") as file:
        words_list = [line.strip().lower() for line in file]

    play_wordle(words_list)
