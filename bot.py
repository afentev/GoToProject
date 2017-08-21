import telebot
token = '335976113:AAG0Z4lhYsLWRZ7KUsvTKRpP2SacaytTn9M'
bot = telebot.TeleBot(token)
id_ = -216295082  # заменить на id беседы, где бот должен работать
users = []
tasks = []


@bot.message_handler(commands=['start'])
def sorry(message):
    bot.send_message(message.chat.id,
                     'Этот бот создан для систематизации жизни лагеря.Список команд можно получить командой /test')


@bot.message_handler(commands=['create_task'])
def new_task(message):
    if message.chat.type == 'group':
        tasks.append(' '.join(message.text.split()[1:]))
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('Я!'))
        print(message)
        bot.send_message(message.chat.id, ' '.join(message.text.split()[1:]), reply_markup=keyboard)
    print(str(tasks))

if __name__ == '__main__':
    bot.polling(none_stop=True)
