import telebot
from config import TOKEN
from handlers.message_handlers import register_handlers

# Инициализация бота с токеном
bot = telebot.TeleBot(TOKEN)

# Основной запуск
if __name__ == '__main__':
    # Регистрация обработчиков
    register_handlers(bot)

    # Запуск опроса
    bot.polling(none_stop=True)
