#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""JSON, Loops and Functions.  Let the computers do the repetitious work!"""


import json
import os


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "cars.json")) as json_file:
    inventory = json.load(json_file)


# TODO: Use a loop to add up how many sports cars we have in stock
total_sports_cars = 0


# TODO: Complete the function so that it returns the available stock
def stock(make: str, model: str) -> int:
    """Get the number of vehicles in stock from the inventory."""
    return 0


if __name__ == '__main__':
    print("We have {} sports cars in stock.".format(total_sports_cars))

    print(
        "You want a Dodge Viper?  We have {} of those."
        "".format(stock("Dodge", "Viper"))
    )
