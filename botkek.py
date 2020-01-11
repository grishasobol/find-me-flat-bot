import telebot
from threading import Thread
import time
import cian
import os
import argparse
import googapi

TERMINATE = False
ID = None
data_dir = os.path.join(os.path.dirname(__file__), "data")
KNOWN_PATH = os.path.join(data_dir, 'known.json')
CIAN_URL = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice=35000&offer_type=flat&region=1&room1=1&room2=1&type=4'
TELE_KEY = None
GOOGLE_KEY = None

class CianParser(Thread):
    def __init__( self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run( self):
        print "START CIAN PARSER"
        while not TERMINATE:
            time.sleep(1)

            if not ID:
                continue

            refs, page_links = cian.parse(KNOWN_PATH, CIAN_URL)
            if refs:
                print refs
            for ref in refs:
                self.bot.send_message( ID, ref )
            time.sleep( 60 )


def main():
    parser = argparse.ArgumentParser(description='wrapper')
    parser.add_argument('--telekey', help='API key for lelegram bot', required=True)
    parser.add_argument('--googlekey', help='API key for google services')
    args = parser.parse_args()

    global TELE_KEY
    TELE_KEY = args.telekey
    global GOOGLE_KEY
    GOOGLE_KEY = args.googlekey

    google = googapi.GoogleAPI( GOOGLE_KEY )
    bot = telebot.TeleBot( TELE_KEY )

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        global ID
        ID = message.chat.id
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(commands=['time'])
    def send_time(message):
        bot.reply_to(message, google.get_travel_time('Moscow', 'Protvino'))

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
