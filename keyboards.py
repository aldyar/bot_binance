from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Старт мониторинга🚀'),
                                     KeyboardButton(text= 'Стоп⏸️')]],
                           resize_keyboard=True,input_field_placeholder='Выберите пункт меню.')