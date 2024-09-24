from telebot import TeleBot
from keyboards.reply_keyboards import hairstyle_keyboard, decision_keyboard
from utils.data_manager import user_data, save_user_data
from config import HAIRSTYLE_IMAGES


def register_handlers(bot: TeleBot):
    bot.message_handler(commands=['start'])(lambda message: start_survey(bot, message))
    bot.message_handler(func=lambda message: True)(lambda message: handle_all_messages(bot, message))


def start_survey(bot: TeleBot, message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    msg = bot.send_message(chat_id, "Добро пожаловать в нашу парикмахерскую! Как вас зовут?")
    bot.register_next_step_handler(msg, lambda m: process_name_step(bot, m))


def process_name_step(bot: TeleBot, message):
    chat_id = message.chat.id
    name = message.text
    save_user_data(chat_id, 'name', name)
    show_hairstyle_options(bot, chat_id)


def show_hairstyle_options(bot: TeleBot, chat_id):
    markup = hairstyle_keyboard()
    msg = bot.send_message(chat_id, "Выберите тип стрижки:", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: process_hairstyle_choice(bot, m))


def process_hairstyle_choice(bot: TeleBot, message):
    chat_id = message.chat.id
    choice = message.text
    if choice in HAIRSTYLE_IMAGES:
        send_hairstyle_image(bot, chat_id, choice)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите стрижку из предложенных вариантов.")
        show_hairstyle_options(bot, chat_id)


def send_hairstyle_image(bot: TeleBot, chat_id, style):
    image_url = HAIRSTYLE_IMAGES[style]
    bot.send_photo(chat_id, image_url)
    markup = decision_keyboard()
    msg = bot.send_message(chat_id, "Вам подходит эта стрижка?", reply_markup=markup)
    save_user_data(chat_id, 'current_style', style)  # Добавленная строка
    bot.register_next_step_handler(msg, lambda m: process_style_decision(bot, m, style))


def process_style_decision(bot: TeleBot, message, current_style):
    chat_id = message.chat.id
    decision = message.text
    if decision == "Подходит":
        save_user_data(chat_id, 'chosen_style', current_style)
        msg = bot.send_message(chat_id,
                               "Отлично! Введите желаемую дату и время для записи (например, 25.09.2024 14:00):")
        bot.register_next_step_handler(msg, lambda m: process_datetime(bot, m))
    elif decision == "Следующая":
        show_hairstyle_options(bot, chat_id)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите 'Подходит' или 'Следующая'.")
        send_hairstyle_image(bot, chat_id, current_style)


def process_datetime(bot: TeleBot, message):
    chat_id = message.chat.id
    datetime = message.text
    save_user_data(chat_id, 'appointment_time', datetime)

    user_info = user_data[chat_id]
    summary = f"Ваша запись:\nИмя: {user_info['name']}\nСтрижка: {user_info['chosen_style']}\n" \
              f"Дата и время: {user_info['appointment_time']}"
    bot.send_message(chat_id, summary)
    bot.send_message(chat_id, "Спасибо за запись! Ждем вас в нашей парикмахерской.")


def handle_all_messages(bot: TeleBot, message):
    chat_id = message.chat.id
    if message.text.lower() in [style.lower() for style in HAIRSTYLE_IMAGES.keys()]:
        process_hairstyle_choice(bot, message)
    elif message.text in ["Подходит", "Следующая"]:
        if 'current_style' in user_data.get(chat_id, {}):
            process_style_decision(bot, message, user_data[chat_id]['current_style'])
        else:
            bot.send_message(chat_id, "Извините, произошла ошибка. Давайте начнем сначала.")
            start_survey(bot, message)
    else:
        bot.send_message(chat_id,
                         "Извините, я не понимаю. Пожалуйста, используйте команду /start для начала записи или выберите один из предложенных вариантов.")