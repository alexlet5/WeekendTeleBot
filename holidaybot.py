import telebot
import random
from telebot import types
import requests
import json
import time
import datetime

bot = telebot.TeleBot('1340374373:AAGnJJaEhO4vrEjjdgNj7BY0KVIPggU1nRE')


spamday = 0       #тупая рассылка(очень тупая(очень(очень))), хвост на 94 строке
while True:

    def to_text(response):  #апи выдает 0 по будням, 1 по выходным
        if (response == 1):
            return("Сегодня выходной")
        else:
            return("Увы, сегодня не выходной ")

    def getyear():
        return str(datetime.datetime.now())[0:4]

    def getmonth():
        return str(datetime.datetime.now())[5:7]

    def getday():
        return str(datetime.datetime.now())[8:10]

    def gethour():
        return str(datetime.datetime.now())[11:13]




    def getid(user):
        return user['chat_id']

    def get_index_of_user(user_id, users):
        for index, user in enumerate(users):
            if user['user_id'] == user_id:
                return index
        return None

    def get_users():
        with open('users.json', 'r') as read_file:
            return json.load(read_file)

    def save_users(users):
        with open('users.json', 'w') as write_file:
            json.dump(users, write_file)

    def spam():                       #вызывает ежедневную рассылку подписчикам
        users = get_users()
        for user in users:
            bot.send_message(getid(user),to_text(requests.get(f'https://isdayoff.ru/{getyear()}{getmonth()}{getday()}')))




    @bot.message_handler(commands=['today'])
    def today(message):
        bot.send_message(message.chat.id, to_text(requests.get(f'https://isdayoff.ru/{getyear()}{getmonth()}{getday()}')))



    @bot.message_handler(commands=['unsubscribe'])
    def unsubscribe(message):
        users = get_users()
        new_users = list(filter(lambda user: user['chat_id'] != message.chat.id, users))
        save_users(new_users)
        bot.send_message(message.chat.id,"Вы успешно отписались от ежедневной рассылки")


    @bot.message_handler(commands=['subscribe'])
    def subscribe(message):
        users = get_users()
        index = get_index_of_user(message.from_user.id, users)
        if index is None:
            users.append({
                'chat_id': message.chat.id,
                'user_id': message.from_user.id,
            })
            save_users(users)
            bot.send_message(message.chat.id,"Вы успешно подписались на ежедневную рассылку")

    @bot.message_handler(commands=['spam']) #админ-команда для принудительной рассылки
    def startspam(message):
        if message.from_user.id == 942733169:  #проверка id админа(меня)
            spam()



    if getday() != spamday:
        if gethour() == str(8):   #рассылка в 8 утра
            spam()
            spamday = getday()




    if __name__ == '__main__':
        bot.polling(none_stop=True)