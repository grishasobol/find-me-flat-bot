import telebot
from threading import Thread
import time
import cian
import os

TERMINATE = False
ID = None
data_dir = os.path.join(os.path.dirname(__file__), "data")
KNOWN_PATH = os.path.join(data_dir, 'known.json')
CIAN_URL = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice=35000&offer_type=flat&region=1&room1=1&room2=1&type=4'

class CianParser(Thread):
    def __init__( self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run( slef):
        print "START CIAN PARSER"
        while not TERMINATE:
            time.sleep(1)
            if ID:
                refs, page_links = cian.parse(KNOWN_PATH, CIAN_URL)
                if refs:
                    print refs
                for ref in refs:
                    bot.send_message( ID, ref )
                time.sleep( 60 )


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
