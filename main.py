import os
from flask import Flask, request
import telebot
from message_analyzer import check_message
from EmailSender import EmailSender
from DbSaver import DataSaver

TOKEN = os.environ.get("TelegramToken")
DOMAIN = os.environ.get("BotDomain")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    hello_message = 'Привет, ' + message.from_user.first_name + "\n"
    hello_message = hello_message + "Бот можно использовать двумя способами:" + "\n" + "1. Ввести название кодекса (ук, УК, уголовный кодекс, Уголовный Кодекс) и номер статьи. Например, ук ст 139, или ук ст.139, или ук статья 139, или ук ст. 139."
    hello_message = hello_message + "\n" + "2. Ввести название кодекса и слово. Я попробую найти это слово в кодексе и покажу все статьи, в которых оно упоминается. Например, ук кража."
    hello_message = hello_message + "\n" + "Подсказка: если ввести ук 20, то я покажу все статьи в УК, в которых есть число 20 либо слово двадцать."
    hello_message = hello_message + "\n" + "Сейчас я работаю с УК, УПК, ГК, ГПК, КоАП, ПИКоАП, ХПК, ТК, КоБС."
    bot.reply_to(message, hello_message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def search_message(message):
    if len(message.text.split(" ")) < 2:
        bot.reply_to(message, "Неправильный формат запроса.")
        return
    answer = check_message(message.text)
    db = DataSaver()
    try:
        if type(answer) == list:
            for item in answer:
                if len(answer) > 4096:
                    for x in range(0, len(answer), 4096):
                        bot.reply_to(message, answer[x:x+4096])
                else:
                    bot.reply_to(message, item)
        else:
            if len(answer) > 4096:
                for x in range(0, len(answer), 4096):
                    bot.reply_to(message, answer[x:x+4096])
            else:
                bot.reply_to(message, answer)
        db.save_request_info(message, "OK")
    except Exception as e:
        db.save_request_info(message, "FAIL")
        email_sender = EmailSender()
        return email_sender.send_email(str(e), message.text)

@server.route('/', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 443)))
    bot.remove_webhook()
    bot.set_webhook(url=DOMAIN)