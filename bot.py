from copy import deepcopy

import telebot
import sqlite3

token = '335976113:AAG0Z4lhYsLWRZ7KUsvTKRpP2SacaytTn9M'
bot = telebot.TeleBot(token)
chat_id = -216295082  # заменить на id беседы, где бот должен работать
users = []
tasks = []


@bot.message_handler(commands=['start'])
def sorry(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Создать задание', callback_data='create_task'),
                 telebot.types.InlineKeyboardButton('Список доступных заданий', callback_data='tasks_list'))
    bot.send_message(message.chat.id,
                     'Этот бот создан для систематизации жизни лагеря.', reply_markup=keyboard)


@bot.message_handler(commands=['create_task'])
def new_task(message):
    if message.chat.type != 'group':
        tasks.append([' '.join(message.text.split()[1:-1]), ' '.join(message.text.split()[-1])])
        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text='Я', callback_data='test')
        keyboard.add(button)
        print(message)
        bot.send_message(message.chat.id, 'Оке', reply_markup=keyboard)
    print(str(tasks))


@bot.callback_query_handler(func=lambda call: True)
def response_inline(call):
    if call.message:
        if call.data == 'create_task':
            users.append(call.from_user.id)
            bot.send_message(call.from_user.id,
                             'Отправьте сообщения следующего формата:\nЗаголовок задания\nКоличество требующихся исполнителей\nДата сдачи')
        for task in tasks:
            if call.data == task[0]:
                bot.send_message(call.from_user.id, 'Ты взялся за выполнение задания')


@bot.message_handler(content_types=['text'])
def handler(message):
    print(users)
    if message.from_user.id in users:
        print(message.text.count('\n'))
        if message.text.count('\n') == 2:
            information = ['{} {}'.format(message.from_user.first_name, message.from_user.last_name)]
            information.extend(deepcopy(message.text.split('\n')))
            users.remove(message.from_user.id)
            chat_notification(information)
        print(users)


@bot.message_handler(commands=['delete'])
def del_task(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(len(tasks)):
        keyboard.add(telebot.types.InlineKeyboardMarkup(tasks[i].text))


def chat_notification(information):
    print(information)
    user, text, count, date = information
    string = '{} создал задание "{}" для {} человек! Задание активно до {}'.format(user, text, count, date)
    print(text, string, sep='\n')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text='Я берусь', callback_data=text))  # FIXME тут какая-то хрень странная, исправьте
    bot.send_message(chat_id=chat_id, text=string, reply_markup=keyboard)

if __name__ == '__main__':
    bot.polling(none_stop=True)
