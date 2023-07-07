#-*-utf8-*-
import sys
import re
import json
from collections import defaultdict

dictionary = sys.argv[1]
biblio = "Амхарско-Русский словарь. Ганкин 1969"
language = "Amharic"

#abbr_file =open("qechua_abr.txt")
#abbr = json.load(abbr_file)

reg = re.compile("\d+\.|\d+\)")

def has_polysemy(line):
    
    if reg.search(line):
        return True
        

def process_dictionary(dictionary):
    with open(dictionary, 'r') as file:
        lines = file.readlines()
    #pomety = []
    output_lines = []
    current_entry = None
    polydict = defaultdict(list)
    commentary = ""
        
    for line in lines:
        line = line.strip()
        if has_polysemy(line):
            parsed_line = re.split(reg, line)
            entry_word = parsed_line[0]
            meanings = parsed_line[1:]
            for meaning in meanings:
                if meaning.strip():
                    meaning = meaning.split(";")[0]
                   
                    
                    polydict[entry_word].append(meaning)
            
            for elem in polydict:
                    meaning1 = polydict[elem][0]
                    for mean in polydict[elem][1:]:
                               current_line = "\t".join([entry_word, meaning1, mean, language, biblio, "-"])
                               output_lines.append(current_line)
                               
                    polydict = defaultdict(list)
                    meaning = ""
                    commentary = ""
                    pomety = []
                    
    return output_lines


# Пример использования
result = process_dictionary(dictionary)
for elem in result:
    print(elem)
