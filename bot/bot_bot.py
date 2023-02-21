import telegram
from decouple import config
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot = telegram.Bot(config('TOKEN'))
updater = Updater(config('TOKEN'), use_context=True)

def start(update, context):
    keyboard = [
        [telegram.KeyboardButton('Go to website')],
        [telegram.KeyboardButton('Live chat')],
        [telegram.KeyboardButton('Get currency exchange')],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

def go_to_website(update, context):
    update.message.reply_text('Here is the website URL: https://www.vb.kg')

def live_chat(update, context):
    update.message.reply_text('Connecting you to live customer service...')

def get_response(update, context):
    url = 'https://24.kg/'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    currency = soup.find('div', class_="currency")
    all_currency = currency.find_all('div')
    curency_data = {}
    for curr in all_currency:
        currency_, rate  = curr.text.split()
        curency_data[currency_] = float(rate)
    response_text = '\n'.join([f"{curr}: {rate}" for curr, rate in curency_data.items()])
    update.message.reply_text(response_text)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.regex('Go to website'), go_to_website))
dispatcher.add_handler(MessageHandler(Filters.regex('Live chat'), live_chat))
dispatcher.add_handler(MessageHandler(Filters.regex('Get currency exchange'), get_response))

updater.start_polling()
updater.idle()
