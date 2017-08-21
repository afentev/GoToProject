import telebot

bot = telebot.TeleBot('335976113:AAG0Z4lhYsLWRZ7KUsvTKRpP2SacaytTn9M')
id_ = -216295082  # заменить на id беседы, где бот должен работать
users = set()


@bot.message_handler(commands=['start'])
def sorry(message):
    bot.send_message(message.chat.id,
                     'Этот бот создан для систематизации жизни лагеря.Список команд можно получить командой /test')


@bot.message_handler(commands=['create_task'])
def new_task(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(content_types=['text'])
def repeat(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
