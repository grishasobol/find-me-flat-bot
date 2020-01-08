import telebot
import gevent 
from threading import Thread

TB = None
ID = None

class CianParser(Thread):
    def __init__( self, bot, )
    while True:
        gevent.sleep(1)
        if ID:
            print ID


def main():
    global TB
    bot = telebot.TeleBot("534840844:AAH-SUIsnwWIjn4IGB9UD-blwegM1iYqXRA")
    TB = bot

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        global ID
        ID = message.chat.id
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.reply_to(message, message.text)

    gevent.joinall([
        gevent.spawn(bot.polling),
        gevent.spawn(cian_parser),
    ])

if __name__ == "__main__":
    main()
