import re
import sys
import sys
import requests
from pymystem3 import Mystem

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", help = "dictionary file")
parser.add_option("-l", "--lang", help = "language name")
parser.add_option("-b", "--biblio", help = "reference (dict name)")
#parser.add_option("-r", "--result", help = "result")

options, args = parser.parse_args()

file = options.file
lang = options.lang
reference = options.biblio
#result = options.result



#NB! то что считается в бамрсе омонимами сейчас не попадает в результат

division = re.compile("\d+\)")


#оставляем только русскую кириллицу. Убираем всю латиницу и монгольские спецсимволы
def clear_text(text):
    new_text = re.sub(r'\(.*\)?', '', text)
    new_text = re.sub(r'[^а-яА-ЯёЁ ]', ' ', new_text)

    return " ".join(new_text.split())

#опасная функция, часто удаляет полезные слова.
def remove_stopwords(text):
    new_text = re.sub(r'\w+\.', '', text)
    return " ".join(new_text.split())

#стопслова из мокшанского словаря
stopwords = ['сущ.', 'многокр.', 'отгл.', 'гл.', 'прил.', 'понуд.', 'возм.', 'уменьш.-ласк.', 'тк.', 'нареч.', 'прич.', 'ед.', 'возвр.', 'диал.', 'перен.', 'П.', 'т.', '(М.', 'М.', 'И.', '(П.', 'Л.', 'С.', 'Пол.)', 'мн.', 'этн.', 'бот.', 'начин.', 'прост.', 'А.', 'зоол.', 'В.', '(И.', 'п.', 'Т.', 'уст.', '(Л.', '(Т.', 'какой-л.', 'чего-л.;', 'какого-л.', 'звукоподр.', '(Посл.)', '(С.', 'Ф.', 'п.;', 'чего-л.', '(А.', 'см.', 'мест.', 'усил.', 'п.)', 'п.);', '(В.', '(букв.', 'собир.', 'сокр.', '(Ф.', 'грам.', 'мед.', 'что-л.', 'числ.', 'п.).', '(Курт.)', 'Зуб.-', '(Н.', 'межд.', 'знач.', 'нареч.-изобр.', '(Зуб.-', 'сказ.', '.', '(Я.', 'уменьш.', 'анат.', 'каких-л.', 'ст.', 'Посл.)', 'мат.', 'вводн.', 'каком-л.', 'Курт.)', 'неопр.', 'кого-л.', 'безл.', 'воен.', 'что-л.;', '(Альк.)', '(Мокш.', 'Пишл.)', 'Муром.)', 'чего-л.,', '(Паёв.)', 'бран.', '(Ст.', '(Промз.)', 'ткац.', 'лингв.', 'М.-', '3.', 'рел.', 'Потьм.)', 'п.,', 'тех.', 'Я.', 'какое-л.', '(Муром.)', '(Булд.)', 'лангс...', 'какую-л.', 'вопр.', '(Калин.)', '(Зубл.-', 'муз.', 'Ю.', 'д.', 'Сам.)', '(Ю.', 'разг.', 'порядк.', '(Инсар.)', '(З.', 'колич.', 'миф.', 'спец.', 'каким-л.', '(см.', 'чем-л.', 'с.-х.', '(Зубл.-Пол.)', 'спорт.', 'кому-л.', '(Глушк.)', '(Зуб.-Пол.)', 'т.п.', 'дет.', 'Мур.)', 'кого-чего-л.;', 'многорк.', 'cyщ.', 'хим.', 'чём-л.', 'какому-л.', 'физ.', 'д.;', 'отриц.', 'Инсар.)', '(Шад.)', 'Пимб.)', 'церк.', 'кем-л.', '(Верхис.)', 'чём-л.;', 'чему-л.;', 'Бадик.)', 'т.п.;', 'уменьш-ласк.', 'что-л.,', 'какие-л.', '(Клоп.)', 'Перхл.)', '(Подг.', 'кого-л.;', '(Атюр.)', 'чем-л.;', 'Н.-', 'Верхис.)', 'Борк.)', '(Кузьм.)', 'Н.', 'Глушк.)', '(Темяш.)', 'кого-чего-л.', 'относ.', 'ист.', 'указ.', 'Кон.)', 'пренебр.', '(Пимб.)', 'д.)', 'неодобр.', '(Левж.)', 'многкор.', 'чему-л.', 'Альк.)',  'притяж.', 'сторону.', 'утв.', 'лит.', 'т.п.,', 'т.п.)', 'фольк.', 'астр.', 'биол.', 'кому-чему-л.', 'кому-л.;',  '(Рыбк.)', 'т.п.).', 'Пош.)', 'др.', '(Фёд.)', 'кого-л.,', 'п.),', 'колга...', 'д.);', 'кем-чем-л.', 'ласк.']
def remove_stopwords_from_list(text):
  new_text = []
  for word in text.split():
    if word in stopwords:
        continue
    else:
       new_text.append(word)
  return " ".join(new_text)

for line in open(file, 'r'):
    if not "1)" in line:
        pass
    elif "үз." in line or "үз;" in line:
        pass
    else:
        line = line.strip().strip(".")
        line = line.replace("¬", "")
        entry = line.split()[0]
        meanings = " ".join(line.split()[1:])
        meanings = remove_stopwords_from_list(meanings)
#        meanings = remove_stopwords(meanings)
        main_meaning = division.split(meanings)[1].split(';')[0]
        main_meaning = clear_text(main_meaning)
        for elem in division.split(meanings)[2:]:
            sense = elem.split(';')[0]
            sense = clear_text(sense)
            if (main_meaning.strip() != "") and (sense.strip() != ""):
                print (f"{entry}\t{main_meaning}\t{sense}\t{lang}\t{reference}")

