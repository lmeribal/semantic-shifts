from bs4 import BeautifulSoup
import urllib.request
from lxml import html
import requests


def get_next_page(url):
    basic_page = requests.get(url)
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    i = 0
    for link in soup.findAll('a'):
        i += 1
        if i == 31:
            next_url = "http://www.devri.bzh"+link.get('href')
    return next_url


def get_next_letter(url):
    if url == "http://www.devri.bzh/dictionnaire/a/azzijun/":
        return "http://www.devri.bzh/dictionnaire/b/b/"

    elif url == "http://www.devri.bzh/dictionnaire/b/bzit/":
        return "http://www.devri.bzh/dictionnaire/ch/cha/"

    elif url == "http://www.devri.bzh/dictionnaire/ch/chutenn/":
        return "http://www.devri.bzh/dictionnaire/c-h/chagn/"

    elif url == "http://www.devri.bzh/dictionnaire/c-h/c_hwedez-c_hweder/":
        return "http://www.devri.bzh/dictionnaire/d/d/"

    elif url == "http://www.devri.bzh/dictionnaire/d/duz/":
        return "http://www.devri.bzh/dictionnaire/e/e-war/"

    elif url == "http://www.devri.bzh/dictionnaire/e/ezwentek/":
        return "http://www.devri.bzh/dictionnaire/f/fa/"

    elif url == "http://www.devri.bzh/dictionnaire/f/fuzuilher/":
        return "http://www.devri.bzh/dictionnaire/g/g/"

    elif url == "http://www.devri.bzh/dictionnaire/g/gwriziennus/":
        return "http://www.devri.bzh/dictionnaire/h/ha-2/"

    elif url == "http://www.devri.bzh/dictionnaire/h/hwi/":
        return "http://www.devri.bzh/dictionnaire/i/i/"

    elif url == "http://www.devri.bzh/dictionnaire/i/izuler/":
        return "http://www.devri.bzh/dictionnaire/j/jabadao/"

    elif url == "http://www.devri.bzh/dictionnaire/j/juzarm/":
        return "http://www.devri.bzh/dictionnaire/k/k.l.t/"

    elif url == "http://www.devri.bzh/dictionnaire/k/kwir/":
        return "http://www.devri.bzh/dictionnaire/l/la-2/"

    elif url == "http://www.devri.bzh/dictionnaire/l/luzius/":
        return "http://www.devri.bzh/dictionnaire/m/m-m/"

    elif url == "http://www.devri.bzh/dictionnaire/m/muzurour/":
        return "http://www.devri.bzh/dictionnaire/n/n-1/"

    elif url == "http://www.devri.bzh/dictionnaire/n/numero/":
        return "http://www.devri.bzh/dictionnaire/o/o/"

    elif url == "http://www.devri.bzh/dictionnaire/o/ozhac_hwreg/":
        return "http://www.devri.bzh/dictionnaire/p/pa-1/"

    elif url == "http://www.devri.bzh/dictionnaire/p/puzuilhan/":
        return "http://www.devri.bzh/dictionnaire/r/ra/"

    elif url == "http://www.devri.bzh/dictionnaire/r/ruzus/":
        return "http://www.devri.bzh/dictionnaire/s/s-1/"

    elif url == "http://www.devri.bzh/dictionnaire/s/sveden/":
        return "http://www.devri.bzh/dictionnaire/t/regentat/"

    elif url == "http://www.devri.bzh/dictionnaire/t/tuzumin/":
        return "http://www.devri.bzh/dictionnaire/u/u-ui/"

    elif url == "http://www.devri.bzh/dictionnaire/u/uzus/":
        return "http://www.devri.bzh/dictionnaire/v/va-1/"

    elif url == "http://www.devri.bzh/dictionnaire/v/vutuner/":
        return "http://www.devri.bzh/dictionnaire/w/wallas/"

    elif url == "http://www.devri.bzh/dictionnaire/w/wut/":
        return "http://www.devri.bzh/dictionnaire/y/ya-eya-ia/"

    elif url == "http://www.devri.bzh/dictionnaire/y/yuzeviezh/":
        return "http://www.devri.bzh/dictionnaire/z/"
    else:
        return 0


def get_text(url):
    session = requests.Session()
    request = session.get(url)
    page_code = request.text
    soup = BeautifulSoup(page_code, 'lxml')
    text_list = soup.find('div', {'class': 'texte'})
    return text_list.text


base = "http://www.devri.bzh/dictionnaire/a/a-1-a-ag-a/"
link = base
check = 1
cur_url = base
test = 0
with open('dict.txt', 'w', encoding='utf-8') as f:
    while cur_url != "http://www.devri.bzh/dictionnaire/z/zrodin/":

        if get_next_letter(cur_url) != 0:
            cur_url = get_next_letter(cur_url)
        else:
            cur_url = get_next_page(cur_url)
        f.write(get_text(cur_url))
        print(get_text(cur_url))
    cur_url = "http://www.devri.bzh/dictionnaire/z/zrodin/"
    f.write(get_text(cur_url))
    f.close()