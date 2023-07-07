#-*-utf8-*-
import sys
import re
import json
from collections import defaultdict

dictionary = sys.argv[1]
biblio = "ACADEMIA MAYOR DE LA LENGUA QUECHUA. DICCIONARIO QUECHUA - ESPAÑOL - QUECHUA. 2005"
language = "Qechua"

abbr_file =open("qechua_abr.txt")
abbr = json.load(abbr_file)


def has_polysemy(line):
    reg = "||" 
    if reg in line:
        return True
        
def extract_pometa(line, pomety):
    try:
        first_token = line.split()[0]
        second_token = line.split()[1]
        if first_token in abbr.keys(): 
            pomety.append(abbr[first_token])
            if second_token in abbr.keys():
                pomety.append(abbr[second_token])
                line = " ".join(line.split()[2:])
            else:
                  line = " ".join(line.split()[1:])
    except:
        pass
    return line, pomety
            

def process_dictionary(dictionary):
    with open(dictionary, 'r') as file:
        lines = file.readlines()
    pomety = []
    output_lines = []
    current_entry = None
    polydict = defaultdict(list)
    commentary = ""
        
    for line in lines:
        line = line.strip()
        if has_polysemy(line):
            entry_word = line.split()[0].strip('\.')
            
            line = " ".join(line.split()[1:])
            line, pomety = extract_pometa(line, pomety)
            meanings = line.split('||')
            for meaning in meanings:
                if meaning.strip():
                    meaning, pomety = extract_pometa(meaning.strip(), pomety)
                    polydict[entry_word].append(meaning)
            
            for elem in polydict:
                    meaning1 = polydict[elem][0]
                    for mean in polydict[elem][1:]:
                               current_line = "\t".join([entry_word, meaning1, mean, language, biblio, "-", " | ".join(pomety)])
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
