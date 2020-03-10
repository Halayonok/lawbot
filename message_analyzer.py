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
    "ba_k" : ['бк', 'Бк', 'БК', 'Банковский кодекс', 'Банковский Кодекс', 'банковский кодекс', 'банковский', 'Банковский'],
    "bu_k" : ['бюк', 'Бюк', 'БЮК', 'бюджетный кодекс', 'Бюджетный кодекс', 'Бюджетный Кодекс', 'бюджетный', 'Бюджетный'],
    "jil_k" : ['жк', 'Жк', 'ЖК', 'жилк', 'жилищный', 'Жилищный кодекс', 'Жилищный Кодекс', 'жилищный кодекс', 'Жилищный'],
    # "k_o_kult" : [],
    "k_o_zemle" : ['коз', 'Коз', 'КОЗ', 'кодекс о земле', 'земельный кодекс', 'земельный', 'Земельный', 'Земельный кодекс', 'Земельный Кодекс', 'О земле', 'о земле'],
    "k_ob_obr" : ['кобр', 'Кобр', 'КОБР', 'кодекс об образовании', 'Кодекс об образовании', 'Кодекс Об Образовании', 'об образовании', 'Об образованиии'],
    "lk" : ['лк', 'Лк', 'ЛК', 'Лесной кодекс', 'Лесной Кодекс', 'лесной кодекс', 'лесной', 'Лесной'],
    "nk" : ['Нк', 'нк', 'НК', 'Налоговый кодекс', 'Налоговый Кодекс', 'налоговый кодекс', 'налоговый', 'Налоговый'],
    "tam_k" : ['тамк', 'Тамк', 'ТАМК', 'таможенный', 'Таможенный', 'таможенный кодекс', 'Таможенный кодекс', 'Таможенный Кодекс', 'таможенный кодекс еаэс', 'ЕЭАС кодекс'],
    "uik" : ['уик', 'Уик', 'УИК', 'уголовно-исполнительный', 'уголовно-исполнительный кодекс', 'Уголовно-исполнительный', 'Уголовно-исполнительный кодекс', 'уголовно-исполнительный Кодекс'],
    "ik" : ['ик', 'Ик', 'ИК', 'избирательный', 'Избирательный', 'избирательный кодекс', 'Избирательный кодекс', 'Избирательный Кодекс', 'избирательный Кодекс'],
    "k_o_nedrah" : ['о недрах', 'О недрах', 'Кодекс о недрах', 'кодекс о недрах', 'Кодекс о Недрах', 'Кодекс О Недрах', 'кодекс о Недрах'],
    "k_o_sud" : ['о судоустройстве', 'О судоустройстве', 'о статусе судей', 'О статусе судей', 'кодекс о судоустройстве', 'Кодекс о судоустройстве', 'Кодекс о статусе судей', 'кодекс о судоустройстве и статусе судей', 'кодекс о статусе судей'],
    "k_torg_more" : ['кодекс мореплавания', 'Кодекс мореплавания', 'о мореплавании', 'О мореплавании', 'Кодекс торгового мореплавания', 'кодекс торгового мореплавания'],
    "vod_k" : ['водный кодекс', 'Водный кодекс', 'водный', 'Водный', 'Водный Кодекс', 'вк', 'Вк', 'ВК'],
    "voz_k" : ['Воздушный', 'воздушный', 'воздушный кодекс', 'Воздушный кодекс', 'Воздушный Кодекс'],
    "k_vnut_vod_tran" : ['Кодекс внутренного водного', 'Кодекс внутренного водного транспорта', 'кодекс внутренного водного', 'кодекс внутренного водного транспорта', 'внутренного водного транспорта', 'Внутренного водного транспорта']
}

empty_results = {
    "uk" : "Уголовном кодексе",
    "gk" : "Гражданском кодексе",
    "gr_pk" : "Гражданском процессуальном кодексе",
    "hoz_pk" : "Хозяйственном процессуальном кодексе",
    "koap" : "Кодексе об административных правонарушениях",
    "kobs" : "Кодесе о браке и семье",
    "pikoap" : "Процессуально-исполнительном кодексе об административных правонарушениях",
    "tk" : "Трудовом кодексе",
    "upk" : "Уголовно-процессуальном кодексе",
    "ba_k" : "Банковском кодекс",
    "bu_k" : "Бюджетном кодексе",
    "jil_k" : "Жилищном кодексе",
    # "k_o_kult" : "",
    "k_o_zemle" : "Кодексе о земле",
    "k_ob_obr" : "Кодексе об образовании",
    "lk" : "Лесном кодексе",
    "nk" : "Налоговом кодексе",
    "tam_k" : "Таможенного кодексе ЕАЭС",
    "uik" : "Уголовно-исполнительном кодексе",
    "ik" : "Избирательном кодексе",
    "k_o_nedrah" : "Кодексе о недрах",
    "k_o_sud" : "Кодексе о судоустройстве и статусе судей",
    "k_torg_more" : "Кодексе торгового мореплавания",
    "vod_k" : "Водном кодексе",
    "voz_k" : "Воздушном кодексе",
    "k_vnut_vod_tran" : "Кодексе внутренного водного транспорта"
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
    article = next((a for a in code if a.startswith(number)), "")
    if len(article) == 0:
        return article
    return f"Статья {article}"

def findWord(word, code, check_cases = True):
    full_articles = []
    articles = []
    if check_cases:
        word = word.lower()
        articles = list(filter(lambda x: word in x and word not in x.split(".")[0], code))
        word = word.capitalize()
        cap_articles = list(filter(lambda x: word in x and word not in x.split(".")[0], code))
        articles.extend([x for x in cap_articles if x not in articles])
    else:
        articles = list(filter(lambda x: word in x and word not in x.split(".")[0], code))
    # if len(articles) > 1:
    #     articles.sort(key=lambda x: x.split(".")[0], reverse=False)
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
                    answer = findArticle(article, articles)
                    if answer is None or len(answer) == 0:
                        return f"В {empty_results[code]} я не нашел статьи {article}"
                    return answer
                else:
                    splitted_message = re.split(f'{code_msg}| ', message)
                    if len(splitted_message) > 3 or not any(w for w in splitted_message if len(w) > 0):
                        return "Неправильный формат запроса!"
                    word = next(w for w in splitted_message if len(w) > 0)
                    articles = splitCode(code)
                    if bool(re.search(r'\d', word)) and "-" not in word and "." not in word:
                        num_word = num2words(word, lang="ru")
                        word_entries = findWord(word, articles, False)
                        num_word_entries = findWord(num_word if len(num_word) < 7 else num_word[:-1], articles)
                        word_entries.extend([x for x in num_word_entries if x not in word_entries])
                        if word_entries is None or len(word_entries) == 0:
                            return f"В {empty_results[code]} я не нашел {word}"
                        return word_entries
                    answer = findWord(word[:-1] if len(word) < 8 else word[:-2], articles)
                    if answer is None or len(answer) == 0:
                        return f"В {empty_results[code]} я не нашел {word}"
                    return answer
        else:
            return "Вы не указали кодекс!"
    except Exception as e:
        email_sender = EmailSender()
        return email_sender.send_email(str(e))