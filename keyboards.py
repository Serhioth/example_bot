from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

btn_1 = KeyboardButton('Проверить')
btn_2 = KeyboardButton('Проверить с даты')
btn_3 = KeyboardButton('Отмена')
kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_1, btn_2, btn_3)
