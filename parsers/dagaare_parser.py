#-*-coding utf-8-*-

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
    new_text = re.sub(r'\d\)', '', text)
    return " ".join(new_text.split())

def remove_markup(text):
    new_text = re.sub(r'\[.*?\]', '', text)
    return " ".join(new_text.split())

polysemic = defaultdict(list)

anycharacter = re.compile("^\w+")
headword = re.compile(r"c blue\](.*) \|\|")
anydigit = re.compile("\(\d+\)")
roman = re.compile(r'\[b\]([IV]+)\[/b\]')
#main_meaning = re.compile("\t\[m1\]1\)")




with codecs.open(file, 'r', 'utf-8') as text_file:
    for line in text_file:
        
        if re.search(anydigit, line):
            meanings = re.search(anydigit, line).groups()
            print (meanings)
#            entry = line.split(anydigit)[0].strip()
#            meaning = line.split(anydigit)[1].strip()
#            if ";" in meaning:
#                meanings = meaning.split(';')
#                for sense in meanings:
#                    polysemic[entry].append(sense)
        else:
            pass
    
comments = "-"

for word in polysemic:
        entry = word
        main = polysemic[word][0]
        for elem in polysemic[word][1:]:
            if entry != "" and main != "" and elem != "":
                print (f"{entry}\t{main}\t{elem}\t{lang}\t{reference}\t{comments}")