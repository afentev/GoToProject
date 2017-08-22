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
                             'Отправьте сообщение следующего формата:\nЗаголовок задания (строка)\nКоличество требующихся исполнителей(натуральное число)\nДата сдачи(ММ.ДД ЧЧ:ММ)')
        for index, task in enumerate(tasks):
            if call.data == task['text'] + 'delete':
                bot.send_message(call.from_user.id, 'Задание "{}" успешно удалено'.format(task['text']))
                for id_ in task['users_accept']:
                    bot.send_message(id_,
                                     'Задание "{}", на выполнение которого вы подписались, было удалено'.format(task['text']))
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(chat_id, 'Задание "{}" было удалено'.format(task['text']))
                del tasks[index]
                break
            elif call.data == task['text'] + 'take':
                tasks[index]['count'] -= 1
                tasks[index]['users_accept'].append('{} {}'.format(call.from_user.first_name, call.from_user.last_name))
                bot.send_message(call.from_user.id, 'Ты взялся за выполнение задания "{}"'.format(task['text']))
                if tasks[index]['count'] == 0:
                    bot.send_message(task['chat.id'],
                                     'Задание "{}" закрыто, так как набралось нужное количество участников'.format(task['text']))
                    del tasks[index]
                break
            elif call.data == task['text'] + 'list':
                if task['users_accept']:
                    bot.send_message(call.from_user.id, text=', '.join(task['users_accept']))
                else:
                    bot.send_message(call.from_user.id, text='За выполнение этого задания еще никто не взялся')
                break



@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == '/delete':
        keyboard = telebot.types.InlineKeyboardMarkup()
        flag = False
        for element in tasks:
            if '{} {}'.format(message.from_user.first_name, message.from_user.last_name) == element['sender_name']:
                keyboard.add(telebot.types.InlineKeyboardButton(element['text'], callback_data=element['text'] + 'delete'))
                flag = True
        if flag:
            bot.send_message(message.chat.id, 'Выберите задание для удаления', reply_markup=keyboard)
    elif message.from_user.id in users:
        if message.text.count('\n') == 2:
            information = {'sender_name': '{} {}'.format(message.from_user.first_name, message.from_user.last_name)}
            information['text'] = message.text.split('\n')[0]
            information['count'] = message.text.split('\n')[1]
            information['date'] = message.text.split('\n')[2]
            information['chat.id'] = message.chat.id
            users.remove(message.from_user.id)
            chat_notification(information)


def chat_notification(information):
    user, text, count, date, chat_id_ = list(information.values())
    try:
        count = int(count)
        date = str(date)
    except ValueError:
        bot.send_message(chat_id=chat_id, text='Неверный формат введенных данных')
        return

    if isinstance(count, int) and isinstance(date, str) and date.count(' ') == 1 and date.split(' ')[0].count('.') == 1\
            and date.split(' ')[1].count(':') == 1:
        string = '{} создал задание "{}" для {} человек! Задание активно до {}'.format(user, text, count, date)
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text='Я берусь', callback_data=text + 'take'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Список взявшихся', callback_data=text + 'list'))
        bot.send_message(chat_id=chat_id, text=string, reply_markup=keyboard)
        information['users_accept'] = []
        tasks.append(information)
        information['count'] = int(information['count'])
    else:
        bot.send_message(chat_id=chat_id_, text='Неверный формат введенных данных')

if __name__ == '__main__':
    bot.polling(none_stop=True)

