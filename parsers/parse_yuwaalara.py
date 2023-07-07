#здесь основная сложность, что словарь сразу на три языка.
import sys
import re
from collections import defaultdict

dictionary = sys.argv[1]
biblio = "A.Ash, J.Giacon, A.Lissarrague. Gamilaraay/Yuwaalaraay/Yuwaalayaay to English Dictionary. 2003"
languages = {"YR": "Yuwaalaraay", "YY": "Yuwaalayaay", "GR": "Gamilaraay"}

      

def extract_meaning(string):
    meaning = ""

    if string and string[0].isdigit() and ('\t' in string):
        meaning = string.split('\t')[1].split('\.')[0]
        meaning, langs = extract_langs_and_words(meaning)
    return meaning, langs

def extract_langs_and_words(string):
    pattern = r"YR|YY|GR"
    pattern1 = r"\(YR|YY|GR\)"
    matches = re.search(pattern, string)
    if matches:
        contents = re.findall(pattern, string)
        langs = [languages[lang.strip()] for lang in contents]
        langs = [l for l in set(langs)]
    else:
        langs = ["Yuwaalaraay", "Yuwaalayaay", "Gamilaraay"]

    # Извлечение части строки перед скобками
    word =  re.split(pattern1, string)[0]
    return word, langs



def process_dictionary(dictionary):
    with open(dictionary, 'r') as file:
        lines = file.readlines()

    output_lines = []
    current_entry = None
    polydict = defaultdict(list)
    
    for line in lines:
        line = line.strip()
        langs= ["Yuwaalaraay", "Yuwaalayaay", "Gamilaraay"]
        if line and not line[0].isdigit():
            current_entry, langs = extract_langs_and_words(line)
        elif line[0].isdigit():
            meaning, meaning_langs = extract_meaning(line)
            polydict[current_entry].append({meaning : meaning_langs})

    for elem in polydict:
        current_entry = elem
        meaning1 = polydict[elem][0].keys()
        for key in meaning1:
            meaning1 = key
            meaning1_langs = polydict[elem][0][meaning1]
            other_meanings = polydict[elem][1:]
            for mean in other_meanings:
                for current_meaning in mean:
                    current_meaning_langs = mean[current_meaning]
                    
                    for lingv in current_meaning_langs:
                        if lingv in meaning1_langs:
                            current_line = "\t".join([current_entry.strip(), meaning1.strip(), current_meaning.strip(), lingv, biblio, "-"])    
                            output_lines.append(current_line)
                        else:
                            current_line = "\t".join([current_entry.strip(), meaning1.strip(), current_meaning.strip(), meaning1_langs[0] + '/' + lingv, biblio, "cognates"])    
                            output_lines.append(current_line)
                            
                           
        
    return output_lines


# Пример использования
result = process_dictionary(dictionary)
for elem in result:
    print(elem)
