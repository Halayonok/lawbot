import re
from EmailSender import EmailSender
from num2words import num2words

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

def get_article(splitted_message):
    for item in splitted_message:
        if bool(re.search(r'\d', item)):
            return item

def is_search_for_article(message):
    art = ["ст", "статья"]
    return bool(re.search(r'\d', message) and any(x for x in art if x in message))

def splitCode(codeName):
    with open(f"/app/{codeName}.txt", 'r', encoding="utf-8") as file:
        prefixes = ("ВА", "ДЕЛ", "НАЯ", "ТЬ")
        data = file.read()
        articles = re.split('Статья |ГЛА|РАЗ|ОСОБЕН|ЧАС', data)
        [articles.remove(s) for s in articles[:] if s.startswith(prefixes) or not s[0].isdigit()]
        return articles

def findArticle(number, code):
    article = next(a for a in code if a.startswith(number))
    return f"Статья {article}"

def findWord(word, code):
    articles = list(filter(lambda x: word in x, code))
    full_articles = []
    for item in articles:
        full_articles.append("Статья " + item + "\n")
    return full_articles

def check_message(message):
    try:
        for code in codes:
            if any(x for x in codes[code] if x in message):
                code_msg = next(code_name for code_name in codes[code] if code_name in message)
                if is_search_for_article(message):
                    splitted_message = re.split(f'{code_msg}|ст.|ст|статья| ', message)
                    article = get_article(splitted_message)
                    articles = splitCode(code)
                    return findArticle(article, articles)
                else:
                    splitted_message = re.split(f'{code_msg}| ', message)
                    if len(splitted_message) > 3 or not any(w for w in splitted_message if len(w) > 0):
                        return "Неправильный формат запроса!"
                    word = next(w for w in splitted_message if len(w) > 0)
                    articles = splitCode(code)
                    if bool(re.search(r'\d', word)) and "-" not in word and "." not in word:
                        num_word = num2words(word, lang="ru")
                        word_entries = findWord(word, articles)
                        num_word_entries = findWord(num_word, articles)
                        return word_entries.extend(x for x in num_word_entries if x not in word_entries)
                    return findWord(word[:-1], articles)
        else:
            return "Вы не указали кодекс!"
    except Exception as e:
        email_sender = EmailSender()
        return email_sender.send_email(str(e), message)