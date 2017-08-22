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
    keyboard.add(telebot.types.InlineKeyboardButton('Создать задание', callback_data='create_task'))
    keyboard.add(telebot.types.InlineKeyboardButton('Список доступных заданий', callback_data='tasks_list'))
    bot.send_message(message.chat.id,
                     'Этот бот создан для систематизации жизни лагеря.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def response_inline(call):
    print(call)
    if call.message:
        print(call.data, tasks)
        if call.data == 'create_task':
            users.append(call.from_user.id)
            bot.send_message(call.from_user.id,
                             'Отправьте сообщения следующего формата:\nЗаголовок задания\nКоличество требующихся исполнителей\nДата сдачи')
        for index, task in enumerate(tasks):
            if call.data == task[1] + 'delete':
                bot.send_message(call.from_user.id, 'Задание "{}" успешно удалено'.format(task[1]))
                for id_ in tasks[tasks.index(task)][-1]:
                    bot.send_message(id_,
                                     'Задание "{}", на выполнение которого вы подписались, было удалено'.format(task[1]))
                bot.delete_message(*task[-2])
                del tasks[index]
            elif call.data == task[1] + 'take':
                tasks[index][-1].append(call.from_user.id)
                bot.send_message(call.from_user.id, 'Ты взялся за выполнение задания "{}"'.format(task[1]))


@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == '/delete':
        keyboard = telebot.types.InlineKeyboardMarkup()
        flag = False
        print(tasks)
        for element in tasks:
            if '{} {}'.format(message.from_user.first_name, message.from_user.last_name) == element[0]:
                keyboard.add(telebot.types.InlineKeyboardButton(element[1], callback_data=element[1] + 'delete'))
                flag = True
        if flag:
            bot.send_message(message.chat.id, 'Выберите задание для удаления', reply_markup=keyboard)
    if message.from_user.id in users:
        if message.text.count('\n') == 2:
            information = ['{} {}'.format(message.from_user.first_name, message.from_user.last_name),
                           [message.chat.id, message.message_id]]
            information.extend(deepcopy(message.text.split('\n')))
            users.remove(message.from_user.id)
            chat_notification(information)


def chat_notification(information):
    user, text, count, date = information
    string = '{} создал задание "{}" для {} человек! Задание активно до {}'.format(user, text, count, date)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text='Я берусь', callback_data=text + 'take'))
    keyboard.add(telebot.types.InlineKeyboardButton(text='Список взявшихся', callback_data=text + 'list'))
    bot.send_message(chat_id=chat_id, text=string, reply_markup=keyboard)
    information.append([])
    tasks.append(information)

if __name__ == '__main__':
    bot.polling(none_stop=True)
