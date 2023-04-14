import telebot

from extensions import Converter
from config import TOKEN, currency_tickets


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду в следующем формате:\n \
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты"
    for currency in currency_tickets.keys():
        text = "\n".join((text, currency,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    base, sym, amount, summ, err = Converter.get_sum(message.text)
    if err:
        bot.reply_to(message, err)
    else:
        bot.reply_to(message, f"Цена {amount} {base} в {sym} :   {round(summ, 2)}")


bot.polling()
