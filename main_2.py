import os
from dotenv import load_dotenv
from telebot import TeleBot, types
import wikipedia

load_dotenv()
API = os.getenv('API')
bot = TeleBot(API)

USER_AGENT = "MyTelegramBot/1.0 (https://example.com; contact@example.com)"
wikipedia.set_lang("ru")
wikipedia.headers = {'User-Agent': USER_AGENT}



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здраствуйте. Напишите то что вы хотите знать с Википедии")


@bot.message_handler(func=lambda message: True)
def search_wikipedia(message):
    query = message.text
    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=False)
        response = f"Поиск '{query}':\n{summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        response = f"Ошибка: {e.options}"
    except wikipedia.exceptions.PageError:
        response = "Такого не существует."

    bot.reply_to(message, response)


bot.polling()
