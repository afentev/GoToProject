import telebot

bot = telebot.TeleBot('335976113:AAG0Z4lhYsLWRZ7KUsvTKRpP2SacaytTn9M')
id_ = -216295082  # заменить на id беседы, где бот должен работать


@bot.message_handler(commands=['create_task'])
def repeat(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(content_types=['text'])
def repeat(message):
    bot.send_message(id_, message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
