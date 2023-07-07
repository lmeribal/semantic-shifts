import sys
import re
from collections import defaultdict

dictionary = sys.argv[1]
biblio = "DEVRI le dictionnaire diachronique du breton - Martial Menard"
language = "Breton"

def extract_meaning(string):
    meaning = ""
    if string and string.startswith('(') and string[1].isdigit():
        try:    
            meaning = re.split(r"\d+\)", string)[1]
            if meaning.strip() == "":
                return False
        except:
            print ("ERRROR", string)
            
        return meaning
    return False




def process_dictionary(dictionary):
    with open(dictionary, 'r') as file:
        lines = file.readlines()

    output_lines = []
    current_entry = None
    polydict = defaultdict(list)
    commentary = ""
    
    for line in lines:
        line = line.strip()
        if line and not current_entry:
            current_entry = line.split('[')[0]
        if line and current_entry:
            if extract_meaning(line): 
               meaning = extract_meaning(line)
               polydict[current_entry].append(meaning)
        if not line:
            for elem in polydict:
                meaning1 = polydict[elem][0]
                for mean in polydict[elem][1:]:
                    if mean != meaning1:
                       current_line = "\t".join([current_entry, meaning1, mean, language, biblio, "-"])
                       output_lines.append(current_line)
            current_entry=None
            polydict = defaultdict(list)
            meaning = ""
            commentary = ""
                
    for elem in polydict:
        meaning1 = polydict[elem][0]
        for mean in polydict[elem][1:]:
            current_line = "\t".join([current_entry, meaning1, mean, biblio])
            output_lines.append(current_line)

    return output_lines


# Пример использования
result = process_dictionary(dictionary)
for elem in result:
    print(elem)
