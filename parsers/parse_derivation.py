#coding: utf-8

import sys
import json
import codecs

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", help = "dictionary file")
parser.add_option("-l", "--lang", help = "language name")
parser.add_option("-b", "--biblio", help = "reference (dict  name)")
parser.add_option("-s", "--separator", help="regex used for separations of the meanings, e.g. \d+\. or \d+\)")
parser.add_option("-e", "--everything", action="store_true", default = False, help="full mode where we take everything as a meaning (with examples)")
#parser.add_option("-r", "--result", help = "result")

options, args = parser.parse_args()

file = options.file
lang = options.lang
separator = options.separator
reference = options.biblio

all_entries = {}


for line in open(file, 'r'):
    try:
             line = line.strip().strip(".")
             line = line.replace("¬", "")
             entry = line.split()[0]
             
             meanings = " ".join(line.split()[1:])
             main_meaning = meanings.split(';')[0]
             if len(entry) < 5:
                pass
             else:
               all_entries[entry] = main_meaning
    except:
        pass
        
substr_dict = {}
#складываем все уже использованный префиксы в множество префиксов
prefix_set = set()

all_keys = set(all_entries.keys())

for key in all_entries.keys():

    prefix = key[:5]
    if not prefix in prefix_set:
        prefix_set.update([prefix])
        for word in all_entries.keys():
            if word.startswith(prefix) and word != key:
                print (f"{key}\t{all_entries[key]}\t{word}\t{all_entries[word]}\t{reference}\tderivation")
