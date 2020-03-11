import os
from flask import Flask, request
import telebot
from message_analyzer import check_message
from EmailSender import EmailSender
from DbSaver import DataSaver
from message_generator import generate_start_message

TOKEN = os.environ.get("TelegramToken")
DOMAIN = os.environ.get("BotDomain")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, generate_start_message(message))
    db = DataSaver()
    db.save_request_info(message, "OK", "OK")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def search_message(message):
    if len(message.text.split(" ")) < 2:
        bot.reply_to(message, "Неправильный формат запроса.")
        return
    answer = check_message(message.text)
    db = DataSaver()
    try:
        if type(answer) == list:
            sleep = False
            if len(answer) > 70:
                bot.reply_to(message, "Похоже, я собрал слишком много информации по Вашему запросу. Попробуйте его конкретизировать.")
                db.save_request_info(message, "Too Many Requests", "OK")
                return
            for item in answer:
                if len(item) > 4096:
                    for x in range(0, len(item), 4096):
                        bot.reply_to(message, item[x:x+4096])
                else:
                    bot.reply_to(message, item)
                if sleep:
                    time.sleep(1)
        else:
            if len(answer) > 4096:
                for x in range(0, len(answer), 4096):
                    bot.reply_to(message, answer[x:x+4096])
            else:
                bot.reply_to(message, answer)
        db.save_request_info(message, "OK", "OK")
    except Exception as e:
        if "Too Many Requests" in str(e):
            bot.reply_to(message, "Похоже, я собрал слишком много информации по Вашему запросу. Попробуйте его конкретизировать.")
        db.save_request_info(message, "FAIL", str(e))
        email_sender = EmailSender()
        return email_sender.send_email(str(e))

@server.route('/', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 443)))
    bot.remove_webhook()
    bot.set_webhook(url=DOMAIN)