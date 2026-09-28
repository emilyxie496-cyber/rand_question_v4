import random

from rand_question_v4.data import questions
from rand_question_v4.data import name_list
from rand_question_v4.selector import rand_draw

def main():
    while True:
        chosen_name, chosen_question = rand_draw(random, name_list, questions)
        print(f"{chosen_name}, please answer: {chosen_question}")

        user_choice = input("Enter 'Y' to continue, or any other key to quit: ")

        if user_choice.upper() != 'Y':
            break
