import re
import pathlib

codes = {
    "uk" : ['ук', 'Ук', 'УК', 'уголовный кодекс', 'Уголовный Кодекс', 'Уголовный кодекс', 'уголовный Кодекс'],
    "gk" : ['гк', 'ГК', 'Гк', 'гражданский кодекс', 'Гражданский Кодекс', 'Гражданский кодекс', 'гражданский Кодекс'],
    "gr_pk" : ['гпк', 'ГПК', 'Гпк', 'гражданский процессуальный кодекс', 'Гражданский Процессуальный Кодекс', 'Гражданский процессуальный кодекс', 'гражданский процессуальный Кодекс', 'гражданский-процессуальный кодекс'],
    "hoz_pk" : ['хпк', 'ХПК', 'Хпк', 'хозяйственный кодекс', 'Хозяйственный Кодекс', 'Хозяйственный кодекс', 'хозяйственный Кодекс', 'хозяйственный процессуальный кодекс', 'Хозяйственный Процессуальный Кодекс', 'Хозяйственный процессуальный кодекс', 'хозяйственный процессуальный Кодекс', 'хозяйственный-процессуальный кодекс'],
    "koap" : ['коап', 'КоАП', 'Коап', 'КОАП'],
    "kobs" : ['кобс', 'Кобс', 'КОБС', 'КоБС', 'кодекс о браке и семье'],
    "pikoap" : ['пикоап', 'ПИКоАП', 'Пикоап', 'ПИКОАП'],
    "tk" : ['ТК', 'Тк', 'тк', 'трудовой кодекс', 'Трудовой кодекс', 'Трудовой Кодекс'],
    "upk" : ['УПК', 'упк', 'Упк', 'уголовный процессуальный кодекс'],
}

def hasArticle(message):
    return bool(re.search(r'\d', message))

def splitCode(codeName):
    with open(f'{pathlib.Path(__file__).parent.absolute()}/{codeName}.txt', 'r', encoding="utf-8") as file:
        prefixes = ("ВА", "ДЕЛ", "НАЯ", "ТЬ")
        data = file.read()
        articles = re.split('Статья |ГЛА|РАЗ|ОСОБЕН|ЧАС', data)
        [articles.remove(s) for s in articles[:] if s.startswith(prefixes) or not s[0].isdigit()]
        return articles

def findArticle(number, code):
    article = next(a for a in code if a.startswith(number))
    return article

def findWord(word, code):
    articles = list(filter(lambda x: word in x, code))
    res = ""
    for item in articles:
        res += "Статья " + item + "\n"
    return res

def check_message(message):
    try:
        for code in codes:
            if any(x for x in codes[code] if x in message):
                if hasArticle(message):
                    message = message.split(" ")
                    for item in message:
                        if hasArticle(item):
                            articles = splitCode(code)
                            return findArticle(item, articles)
                else:
                    message = message.split(" ")
                    for item in message:
                        if item not in codes[code]:
                            articles = splitCode(code)
                            return findWord(item["-1"], articles)
    except Exception as e:
        return str(e)