'''
Filename        : fuzzy_search.py
Author          : Aditya Murray
Date            : 12th July 2016
Det the basics about fuzzy_wuzzy.
'''

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

print 'Simple Ratio'
print 'this is a test, this is a test!'
print fuzz.ratio("this is a test", "this is a test!")

print 'Partial Ratio'
print 'this is a test, this is a test!'
print fuzz.partial_ratio("this is a test", "this is a test!")

print 'Token Sort Ratio'
print "fuzzy wuzzy was a bear, wuzzy fuzzy was a bear"
print fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")

print "fuzzy wuzzy was a bear, wuzzy fuzzy was a bear "
print fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")

print 'Token Set Ratio'
print "fuzzy was a bear fuzzy fuzzy was  a bear"
print fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")

print "fuzzy was a bear fuzzy fuzzy was a bear"
print fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")

print 'Process'
choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
print 'new york jets'
print process.extract("new york jets", choices, limit=2)

print 'cowboys'
print process.extractOne("cowboys", choices)

