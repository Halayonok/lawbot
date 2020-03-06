import os
from flask import Flask, request
import telebot
from message_analyzer import check_message

TOKEN = os.environ.get("TelegramToken")
DOMAIN = os.environ.get("BotDomain")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    hello_message = 'Hello, ' + message.from_user.first_name + "\n"
    hello_message = hello_message + "Бот можно использовать двумя путями:" + "\n" + "1. Ввести название кодекса (ук, уголовный кодекс, Уголовный Кодекс) и номер статьи. Например, ук 139, или ук ст.138, или ук статья 139."
    hello_message = hello_message + "\n" + "2. Ввести нахвание кодекса и слово. Я попробую найти это слово в кодексе и верну все статьи, в которых оно упоминается."
    bot.reply_to(message, hello_message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def search_message(message):
    if message.text == "1":
        return os.path.exists("app/")
    elif message.text == "2":
        return os.path.exists("/app/")
    elif message.text == "3":
        return os.path.exists("//app//")
    elif message.text == "4":
        return os.path.exists("\\app\\")
    elif message.text == "5":
        return os.path.exists("\\app\\")
    elif message.text == "6":
        return os.path.exists("/app/Codes")
    elif message.text == "7":
        return os.path.exists("/app/Codes/")
    elif message.text == "8":
        return os.path.exists("//app/Codes//")
    elif message.text == "9":
        return os.path.exists(f"{os.getcwd()}/Codes/")
    elif message.text == "10":
        return os.path.exists(f"{os.getcwd()}")
    elif message.text == "11":
        return os.path.exists(f"{os.getcwd()}/")
    elif message.text == "12":
        return os.path.exists(f"{os.getcwd()}/Codes")
    elif message.text == "13":
        return os.path.exists(f"{os.getcwd()}/Codes")
    elif message.text == "14":
        return os.path.exists(f"{os.getcwd()}/Codes")
    elif message.text == "15":
        return os.path.exists(f"{os.getcwd()}/Codes")
    elif message.text == "16":
        return os.path.exists(f"{os.getcwd()}/Codes")
    elif message.text == "17":
        return os.path.exists(f"{os.getcwd()}/Codes")
    elif message.text == "18":
        return os.path.exists(f"{os.getcwd()}/Codes")
    elif message.text == "19":
        return os.path.exists("app/uk.txt")
    elif message.text == "20":
        return os.path.exists("/app/uk.txt")
    elif message.text == "21":
        return os.path.exists(f"{os.getcwd()}/uk.txt")
    elif message.text == "22":
        return os.path.exists(f"{os.getcwd()}/Codes/uk.txt")
    elif message.text == "23":
        return os.path.exists("app/Codes/uk.txt")
    else:
        return "100"
    # answer = check_message(message.text)
    # bot.reply_to(message, answer)

@server.route('/', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 443)))
    bot.remove_webhook()
    bot.set_webhook(url=DOMAIN)