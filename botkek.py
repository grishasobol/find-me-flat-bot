import telebot
from threading import Thread
import time

TERMINATE = False
ID = None

class CianParser(Thread):
    def __init__( self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run( slef):
        print "START CIAN PARSER"
        while not TERMINATE:
            time.sleep(1)
            if ID:
                print ID

def main():
    bot = telebot.TeleBot("534840844:AAH-SUIsnwWIjn4IGB9UD-blwegM1iYqXRA")

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        global ID
        ID = message.chat.id
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.reply_to(message, message.text)


    cian_parser = CianParser( bot )
    cian_parser.daemon = True
    cian_parser.start()
 
    print "START TELE BOT "
    bot.polling()

    global TERMINATE
    TERMINATE = True

    print "Wait cian parser"
    cian_parser.join()


if __name__ == "__main__":
    main()
