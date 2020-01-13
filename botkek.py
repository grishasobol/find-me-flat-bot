import telebot
from threading import Thread
import time
import cian
import os
import argparse
import googapi
import re
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TERMINATE = False
ID = None
data_dir = os.path.join(os.path.dirname(__file__), "data")
KNOWN_PATH = os.path.join(data_dir, 'known.json')
CIAN_URL = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice=35000&offer_type=flat&region=1&room1=1&room2=1&type=4'
TELE_KEY = None
GOOGLE_KEY = None
GOOGLE_API = None
USE_GOOGLE_API = True
POINTS = []


def safe_reply_to( bot, message, answer):
    try:
        bot.reply_to( message, answer )
        return True
    except:
        print 'Want to send:\n{}\nBut cannot access telegram =('.format( answer )
        return False

def safe_send_message( bot, chat_id, message):
    try:
        bot.send_message( chat_id, message )
        return True
    except:
        print 'Want to send:\n{}\nBut cannot access telegram =('.format( message )
        return False

def flat_info( ref ):
    data = cian.get_page( ref )
    address = unicode(re.search( '<div data\-name\=\"Geo\".*?content=\"(.*?)\"', data ).group(1))
    info = { 'address': address }
    for point in POINTS:
        info[point[0]] = GOOGLE_API.get_travel_time( address, point[0] )
    return info

def flat_is_suitable( info ):
    for point in POINTS:
        if int(point[1]) < info[point[0]]:
            return False
    return True

def flat_info_to_str( flat_info ):
    info = flat_info.copy()
    answer = 'Address: {}\n'.format( info.pop('address', None) )
    for k in info.keys():
        answer += 'Time = {}min for {}\n'.format( info[k], k)
    return answer


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
            try:
                refs, page_links = cian.parse(KNOWN_PATH, CIAN_URL)
            except:
                continue
            if refs:
                print refs
            for ref in refs:
                if TERMINATE:
                    break
                answer = ref
                if USE_GOOGLE_API:
                    try:
                        info = flat_info( ref )
                        if not flat_is_suitable( info ):
                            continue
                        answer += '\n' + flat_info_to_str( info )
                    except:
                        print 'Cannot get flat info {}'.format( ref)
                        continue
                safe_send_message( self.bot, ID, answer )
                if USE_GOOGLE_API:
                    time.sleep( 30 )
            time.sleep( 60 )




def main():
    parser = argparse.ArgumentParser(description='wrapper')
    parser.add_argument('--cianurl', help='Ref to cian web site search', required=True)
    parser.add_argument('--telekey', help='API key for lelegram bot', required=True)
    parser.add_argument('--googlekey', help='API key for google services')
    args = parser.parse_args()

    global CIAN_URL
    CIAN_URL = args.cianurl
    global TELE_KEY
    TELE_KEY = args.telekey
    global GOOGLE_KEY
    GOOGLE_KEY = args.googlekey

    global GOOGLE_API
    GOOGLE_API = googapi.GoogleAPI( GOOGLE_KEY )
    bot = telebot.TeleBot( TELE_KEY )


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        global ID
        ID = message.chat.id
        safe_reply_to( bot, message, "Hello!!!, I'm starting to search flat for you")

    @bot.message_handler(commands=['addpoint'])
    def addpoint(message):
        s = message.text
        m = re.search('\/addpoint (.*)', s)
        try:
            point = m.group(1)
            point = json.loads(point)
            int(point[1])
        except:
            safe_reply_to( bot, message, 'Ivalid message')
            return

        POINTS.append( point )
        bot.reply_to( message, 'Add new point with address: {}; and time: {}'.format( point[0], point[1]))

    @bot.message_handler(commands=['info'])
    def send_info(message):
        s = message.text
        try:
            ref = re.search( '\/info (.*)', s).group(1)
            info = flat_info( ref )
            answer = 'INFO FOR ' + ref + '\n'
            answer += flat_info_to_str( info )
            bot.reply_to(message, answer)
        except:
            safe_reply_to( bot, message, '=((( cannot collect info')


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
