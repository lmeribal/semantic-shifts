import sys
from collections import defaultdict

dictionary = sys.argv[1]
biblio = "Barry Alpher. Yir-Yoront Lexicon. 1991"
language = "Yir-Yoront"

def extract_meaning(string):
    if string and string[0].isdigit() and ('\t' in string):
        meaning = []
        commentary = []
        preliminary_meaning = string.split('\t')[1].split("Note")[0]
        if "SCI" in preliminary_meaning:
            preliminary_commentary = preliminary_meaning.split("SCI")[1]
            for word in preliminary_commentary.split():
                if not word.isupper():
                    commentary.append(word)
                else:
                #добавляем капитализированные слова после пометы
                    if word.isupper():
                        meaning.append(word)
                    else:
                        break
            commentary = " ".join(commentary)
            
        else:    
            for word in preliminary_meaning.split():
                if word.isupper():
                    meaning.append(word)
                else:
                    break
        meaning = " ".join(meaning)
        if meaning.strip() == "":
            return False
        return meaning, commentary
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
        if line:
            if line.split()[0].isupper():
                for elem in polydict:
                        meaning1 = polydict[elem][0]
                        for mean in polydict[elem][1:]:
                           current_line = "\t".join([current_entry, meaning1, mean, language, biblio, "-"])
                           output_lines.append(current_line)
                           
                current_entry = line.split()[0]
                
                polydict = defaultdict(list)
                meaning = ""
                commentary = ""
                
            if extract_meaning(line): 
               meaning, commentary = extract_meaning(line)
               polydict[current_entry].append(meaning)
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
