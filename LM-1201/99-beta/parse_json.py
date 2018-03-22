#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hands-on parsing JSON in Python"""


import json
import os


here = os.path.abspath(os.path.dirname(__file__))


# Getting JSON text from a file
with open(os.path.join(here, "cars.json")) as json_file:
    json_text = json_file.read()


# What type of data is JSON?
print("json_text is a", type(json_text))


# Python handles the JSON parsing for you
json_data = json.loads(json_text)


# TODO: Print out the data type of the json_data object


# TODO: Write a for loop that prints out all of the makes and models
