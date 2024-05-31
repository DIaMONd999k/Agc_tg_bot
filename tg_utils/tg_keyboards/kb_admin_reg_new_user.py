from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

new_user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Зарегистрировать'
            )
            ],
[
            KeyboardButton(
                text='Отклонить'
            )
            ]
        ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Для продолжения нажмите кнопку внизу'
)

find_in_loodsman_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Да'
            )
            ],
[
            KeyboardButton(
                text='Нет'
            )
            ]
        ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Для продолжения нажмите кнопку внизу'
)
