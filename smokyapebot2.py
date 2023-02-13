import telebot
from telebot import types
import pycoingecko
from pycoingecko import CoinGeckoAPI
from py_currency_converter import convert
cg = CoinGeckoAPI()

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_help_message(message):
    bot.send_message(message.chat.id, f"🐵 Добро пожаловать, {message.chat.username} 🍌"
                                      f"\n"
                                      f"\n Я - эйп-бот, который поможет тебе узнать текущий курс "
                                      f"любой монеты и конвертировать одно в другое по актуальному "
                                      f"курсу! Для продолжения введи команду "
                                      f"/crypto"
                                      f"\n"
                                      f"\n По всем вопросам пиши @smokyape ")

@bot.message_handler(commands=['crypto'])
def main(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('✅ Узнать текущий курс крипты'))
    b1.add(types.KeyboardButton('❎ Узнать текущий курс фиата'))
    cr = bot.send_message(message.chat.id, 'Ты на главной странице бота. \n\n'
                                           'Чтобы узнать текущий курс крипты или фиата,'
                                           'конвертировать валюту выбери соответствующую кнопку: ', reply_markup=b1)
    bot.register_next_step_handler(cr, step1)

def step1(message):
    if message.text == '✅ Узнать текущий курс крипты':
        step2(message)
    elif message.text == '❎ Узнать текущий курс фиата':
        fiat(message)

def fiat(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('❗Главная'),
           types.KeyboardButton('💰Курс USD$'),
           types.KeyboardButton('💰Курс RUB₽'))
    q = bot.send_message(message.chat.id, 'Здесь ты можешь выбрать актуальный курс'
                                          ' в соотношении 1 единица валюты = цена', reply_markup=b1)
    bot.register_next_step_handler(q, fiat_step2)

def fiat_step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('⬅ Вернуться назад'))
    if message.text == '💰Курс USD$':
        price = convert(base='USD', amount=1, to=['RUB', 'EUR', 'AED', 'CHF', 'GBP'])
        bot.send_message(message.chat.id, f'◽ 1 USD$ = {price["RUB"]} ₽ - Рубль \n'
                                          f'◽ 1 USD$ = {price["EUR"]} € - Евро \n'
                                          f'◽ 1 USD$ = {price["AED"]} DH - Дирхам \n'
                                          f'◽ 1 USD$ = {price["CHF"]} ₣ - Франк \n'
                                          f'◽ 1 USD$ = {price["GBP"]} £ - Фунт')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)

    elif message.text == '💰Курс RUB₽':
        price = convert(base='RUB', amount=1, to=['USD', 'EUR', 'AED', 'CHF', 'GBP'])
        bot.send_message(message.chat.id, f'🔸 1 RUB₽ = {price["USD"]} $ - Доллар \n'
                                          f'🔸 1 RUB₽ = {price["EUR"]} € - Евро \n'
                                          f'🔸 1 RUB₽ = {price["AED"]} DH - Дирхам \n'
                                          f'🔸 1 RUB₽ = {price["CHF"]} ₣ - Франк \n'
                                          f'🔸  1 RUB₽ = {price["GBP"]} £ - Фунт')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)

    elif message.text == '❗Главная':
        main(message)

def step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('❗Главная'),
           types.KeyboardButton('💰Курс к USD$'),
           types.KeyboardButton('💰Курс к RUB₽'))
    q = bot.send_message(message.chat.id, 'Здесь ты можешь выбрать актуальный курс'
                                          ' в соотношении монета = цена $/₽', reply_markup=b1)
    bot.register_next_step_handler(q, step3)

def step3(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('⬅ Вернуться назад'))
    if message.text == '💰Курс к USD$':
        price = cg.get_price(ids='bitcoin, ethereum, litecoin, the-open-network, aptos, optimism,'
                                 'matic-network, fantom, solana, polkadot, tether,'
                                 'okb, usd-coin', vs_currencies='usd')
        bot.send_message(message.chat.id, f'📌 Самые популярные монеты: \n\n'
                                          f'🔺 Bitcoin = {price["bitcoin"]["usd"]} $\n'
                                          f'🔺 Ethereum = {price["ethereum"]["usd"]} $\n'
                                          f'🔺 Litecoin = {price["litecoin"]["usd"]} $\n'
                                          f'🔺 TON = {price["the-open-network"]["usd"]} $\n'
                                          f'🔺 Aptos = {price["aptos"]["usd"]} $\n'
                                          f'🔺 Optimism = {price["optimism"]["usd"]} $\n'
                                          f'🔺 Polygon = {price["matic-network"]["usd"]} $\n'
                                          f'🔺 Fantom = {price["fantom"]["usd"]} $\n'
                                          f'🔺 Solana = {price["solana"]["usd"]} $\n'
                                          f'🔺 Polkadot = {price["polkadot"]["usd"]} $\n'
                                          f'🔺 Tether = {price["tether"]["usd"]} $\n'
                                          f'🔺 OKB = {price["okb"]["usd"]} $\n'
                                          f'🔺 USD Coin = {price["usd-coin"]["usd"]} $\n', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == '💰Курс к RUB₽':
        price = cg.get_price(ids='bitcoin, ethereum, litecoin, the-open-network, aptos, optimism,'
                                 'matic-network, fantom, solana, polkadot, tether,'
                                 'okb, usd-coin', vs_currencies='rub')
        bot.send_message(message.chat.id, f'🧿 Самые популярные монеты: \n\n'
                                          f'🔹Bitcoin = {price["bitcoin"]["rub"]} ₽\n'
                                          f'🔹Ethereum = {price["ethereum"]["rub"]} ₽\n'
                                          f'🔹Litecoin = {price["litecoin"]["rub"]} ₽\n'
                                          f'🔹TON = {price["the-open-network"]["rub"]} ₽\n'
                                          f'🔹Aptos = {price["aptos"]["rub"]} ₽\n'
                                          f'🔹Optimism = {price["optimism"]["rub"]} ₽\n'
                                          f'🔹Polygon = {price["matic-network"]["rub"]} ₽\n'
                                          f'🔹Fantom = {price["fantom"]["rub"]} ₽\n'
                                          f'🔹Solana = {price["solana"]["rub"]} ₽\n'
                                          f'🔹Polkadot = {price["polkadot"]["rub"]} ₽\n'
                                          f'🔹Tether = {price["tether"]["rub"]} ₽\n'
                                          f'🔹OKB = {price["okb"]["rub"]} ₽\n'
                                          f'🔹USD Coin = {price["usd-coin"]["rub"]} ₽\n', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == '❗Главная':
        main(message)

bot.polling(none_stop=True)