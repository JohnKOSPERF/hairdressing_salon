from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import HAIRSTYLE_IMAGES

def hairstyle_keyboard():
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for style in HAIRSTYLE_IMAGES.keys():
        markup.add(KeyboardButton(style))
    return markup

def decision_keyboard():
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(KeyboardButton("Подходит"), KeyboardButton("Следующая"))
    return markup
