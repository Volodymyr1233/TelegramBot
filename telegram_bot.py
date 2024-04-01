import random
import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup
import sqlite3





url1 = 'https://maximum.fm/anekdoti-pro-shkolu_n160120'
object1 = requests.get(url1).text
soup1 = BeautifulSoup(object1, 'html.parser')


sup1 = soup1.find_all('p')
result_school = sup1[random.randint(5,len(sup1)-1)].get_text().strip()

lst = []
for i in range(6, len(sup1)):
    if (sup1[i].get_text().strip() == '***'.strip()) or (sup1[i].get_text().strip() == 'Вчителька:'.strip()) or (sup1[i].get_text().strip() == 'В школі:'.strip()):
        pass
    else:
        lst.append(sup1[i].get_text().strip())


url = 'https://maximum.fm/anekdoti-pro-politiku-i-politikiv-aktualni-zharti-pro-nabolile_n157710'
object = requests.get(url).text
soup = BeautifulSoup(object, 'html.parser')


sup = soup.find_all('p')

lst1 = []
for a in range(6, len(sup)):
    if (sup[a].get_text().strip() == '***'.strip()) or (sup[a].get_text().strip() == 'Кумедні меми: Якби князі Київської Русі балотувалися на вибори 2019'.strip()) or (sup[a].get_text().strip() == 'В школі:'.strip()):
        pass
    else:
        lst1.append(sup[a].get_text().strip())

markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('Анекдот про школу')
itembtn2 = types.KeyboardButton('Анекдот про політику')
markup.add(itembtn1, itembtn2)



bot = telebot.TeleBot("7014955344:AAG6I4sKT5QMXap_YWXsZc5sIB2xQSc2Nbc")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    connect = sqlite3.connect('telegram_bot.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS tab(
        first_name TEXT,
        last_name TEXT,
        chat_id INTEGER,
        PRIMARY KEY(chat_id)
)
""")

    connect.commit()
    user_first_name = message.from_user.first_name
    user_last_name =  message.from_user.last_name
    bot.send_message(message.chat.id, str(message.from_user.first_name)+ ', виберіть будь ласка категорію анекдоту, яка Вас цікавить!', reply_markup=markup)

    try:
        lt = [user_first_name, user_last_name, message.chat.id]
        cursor.execute("INSERT  INTO tab VALUES(?, ?, ?);", lt)
        connect.commit()
        bot.send_message(message.chat.id, "Вас записано в базу даних")
    except:
        bot.send_message(message.chat.id, "Ви вже э в базі даних(якщо це цікаво)")



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if (message.text == 'Анекдот про школу'):
        bot.send_message(message.chat.id, str((lst[random.randint(0, len(lst)-1)])), parse_mode='html', reply_markup=markup)
    elif message.text == 'Анекдот про політику':
        bot.send_message(message.chat.id, str((lst1[random.randint(0, len(lst1)-1)])), parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Натисніть будь ласка на кнопки", reply_markup=markup)


if __name__ == "__main__":
     bot.polling(none_stop=True)
