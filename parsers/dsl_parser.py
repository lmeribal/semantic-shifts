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



polysemic = defaultdict(list)

anycharacter = re.compile("^\w+")
anydigit = re.compile("\d+\)")
roman = re.compile(r'\[b\]([IV]+)\[/b\]')
#main_meaning = re.compile("\t\[m1\]1\)")


#если есть словарь сокращений технических помет вида _abrv.dsl, то забираем их оттуда и чистим файл. Может понадобиться поменять кодировку на utf-8.
if options.abbrev:
    stopwords = set()
    with codecs.open(options.abbrev, 'r', 'utf-8') as sw:
        try:
            for line in sw:
                if re.search(anycharacter, line):
                    try:
                        stopwords.update([line.strip()])
                    except:
                        pass
        except:
            pass

def remove_stopwords(text):
    newline = []
    for word in text.split():
        if word.strip() not in stopwords:
           newline.append(word)
    res = " ".join(newline)
    return res

    new_text = re.sub(r'\w+\.', '', text)
    return " ".join(new_text.split())


with codecs.open(file, 'r', 'utf-8') as dsl:
    newentry = None 
    for line in dsl:
        if re.search(anycharacter, line):
            entry = line.strip()
            entry = re.sub("\[.*?\]", "", entry)
            newentry = None

        else:
            try:
                
                if re.search(roman, line):
                    newentry = entry + "_" + re.findall(roman, line)[0]
                    
                if re.search(anydigit, line):
                    line = re.sub("\[.*?\]", "", line).strip()
                    if options.abbrev:
                        line = remove_stopwords(line)
                    line = clear_text(line)
                    if len(line) > 2:
                        if newentry:
                            polysemic[newentry].append(line)
                        else:
                            polysemic[entry].append(line)
                else:
                    if newentry:
                        if options.abbrev:
                            line = remove_stopwords(line)
                        if "[trn]" in line:
                            line = re.sub("\[.*?\]", "", line).strip()
                            line = clear_text(line)
                            if  len(line) > 2:
                                polysemic[newentry].append(line)
                    
                 
            except:
#                    print ("broken line", line)
                    pass

comments = "-"

#первый прогон, не заморачиваясь про омонимы

for word in polysemic:
        entry = word
        main = polysemic[word][0]
        for elem in polysemic[word][1:]:
            if entry != "" and main != "" and elem != "":
                print (f"{entry}\t{main}\t{elem}\t{lang}\t{reference}\t{comments}")

#второй прогон, добываем омонимы
homonym_dict = defaultdict(list)
comments = "homonym"

for homonym in polysemic:
    if "_" in homonym:
        entry = homonym.split("_")[0]
        #добавляем основное значение каждого омонима в список
        homonym_dict[entry].append(polysemic[homonym][0])
        
     
for homonym_word in homonym_dict:
        entry = homonym_word
        main = homonym_dict[homonym_word][0]
        for elem in homonym_dict[homonym_word][1:]:
            if entry != "" and main != "" and elem != "":
                print (f"{entry}\t{main}\t{elem}\t{lang}\t{reference}\t{comments}")