'''
Filename        : fuzzy_search.py
Author          : Aditya Murray
Date            : 12th July 2016
Det the basics about fuzzy_wuzzy.
'''

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

print 'Simple Ratio'
fuzz.ratio("this is a test", "this is a test!")

print 'Partial Ratio'
fuzz.partial_ratio("this is a test", "this is a test!")

print 'Token Sort Ratio'
fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")

fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")

print 'Token Set Ratio'
fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")

print 'Process'
choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
process.extract("new york jets", choices, limit=2)

process.extractOne("cowboys", choices)

