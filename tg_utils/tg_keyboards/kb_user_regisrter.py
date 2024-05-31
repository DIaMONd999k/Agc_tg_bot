from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reg_button = InlineKeyboardButton(
    text='Зарегистрироваться в Боте',
    callback_data='start_registry'
                )

register_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [reg_button]
]
                )

request_phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Отправить номер телефона',
                request_contact=True
            ),
            KeyboardButton(
                text='Отказаться'

            ),
            KeyboardButton(
                text='Ввести номер вручную'

            ),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
