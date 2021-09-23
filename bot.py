import telebot
from config import api_key
import time
import sqlite3

conn = sqlite3.connect('baz_bot.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS questions(
   question INT,
   answer TEXT);
""")
conn.commit()


bot = telebot.TeleBot(api_key)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('баланс', 'банк')
print('start')
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower() == 'запись':
        bot.send_message(message.from_user.id, 'Ведите вопрос', reply_markup=keyboard1)
        print('введите вопрос')
    elif message.text.lower().split()[0].isdigit() == True:
        bot.send_message(message.from_user.id, 'задание '+ message.text, reply_markup=keyboard1)
        print('задание')

    else:
        print(message.text)
        print(message.text.split('ответ1')[0].split())
        print(message.text.split('ответ1')[0])
        print(message.text.split('ответ1'))
        bot.send_message(message.from_user.id, 'Напиши чтобы получить ответ', reply_markup=keyboard1)

bot.polling(none_stop=True, interval=0)