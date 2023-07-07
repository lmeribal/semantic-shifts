#-*-coding:utf-8-*-
"""
A parser for dsl dictionaries
First of all you need to change dsl-file coding to utf-8
"""
import codecs
import re
import sys

from collections import defaultdict

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", help = "dictionary file")
parser.add_option("-l", "--lang", help = "language name")
parser.add_option("-b", "--biblio", help = "reference (dict  name)")
parser.add_option("-a", "--abbrev", help = "stopwords list")

options, args = parser.parse_args()

file = options.file
lang = options.lang
reference = options.biblio



#оставляем только русскую кириллицу. Убираем всю латиницу
def clear_text(text):
    new_text = re.sub(r'\(.*\)?', '', text)
    new_text = re.sub(r'[^а-яА-ЯёЁ ]', ' ', new_text)

    return " ".join(new_text.split())

def remove_markup(text):
    new_text = re.sub(r'\[.*?\]', '', text)
    return " ".join(new_text.split())

polysemic = defaultdict(list)

anycharacter = re.compile("^\w+")
headword = re.compile(r"c blue\](.*) \|\|")
anydigit = re.compile("\d+\)")
roman = re.compile(r'\[b\]([IV]+)\[/b\]')
#main_meaning = re.compile("\t\[m1\]1\)")




with codecs.open(file, 'r', 'utf-8') as dsl:
    entry = None
    for line in dsl:
        if entry:
            meaning = remove_markup(line)
            if ";" in meaning:
                meanings = meaning.split(';')
                for sense in meanings:
                    polysemic[entry].append(sense)
            entry = None
        else:
            potential_entry = re.findall(headword, line)
            if len(potential_entry) > 0:
                 entry = potential_entry[0]


comments = "-"

#первый прогон, не заморачиваясь про омонимы

for word in polysemic:
        entry = word
        main = polysemic[word][0]
        for elem in polysemic[word][1:]:
            if entry != "" and main != "" and elem != "":
                print (f"{entry}\t{main}\t{elem}\t{lang}\t{reference}\t{comments}")