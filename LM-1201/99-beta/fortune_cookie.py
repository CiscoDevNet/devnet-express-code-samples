#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script flow and debugging. Print your own fortune cookie!"""


import random


FORTUNES = [
    "There is a good chance your code will work, eventually.",
    "The weather will be hot, cold or just right today.",
    "I see Network DevOps in your future.",
]


def get_fortune():
    """Use mystical forces (a random selection) to get a user's fortune."""
    return random.choice(FORTUNES)


def get_lucky_numbers(how_many: int) -> list:
    """Returns a list of (random) 'lucky' numbers."""
    lucky_numbers = []
    for _ in range(how_many):
        lucky_numbers.append(random.randint(0, 99))
    return lucky_numbers


def message(fortune: str, lucky_numbers: list) -> str:
    """Create a fortune cookie message."""
    # TODO: Create the fortune cookie message
    fortune_cookie_message = ""
    return fortune_cookie_message


def fortune_cookie(number_of_lucky_numbers: int):
    """Create and print a fortune cookie."""
    fortune = get_fortune()
    lucky_numbers = get_lucky_numbers(number_of_lucky_numbers)
    print(message(fortune, lucky_numbers))


if __name__ == '__main__':
    print("Welcome to the  🥠  script!")

    how_many_lucky_numbers = 0
    while how_many_lucky_numbers < 1:
        how_many_lucky_numbers = input(
            "How many lucky numbers would you like?  "
        )
        try:
            how_many_lucky_numbers = int(how_many_lucky_numbers)
        except ValueError:
            print("Come on... You have to give me a positive number.")

    # TODO: Call the `fortune_cookie()` function
