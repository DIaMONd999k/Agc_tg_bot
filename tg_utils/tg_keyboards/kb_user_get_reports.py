from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

register_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Посмотреть мои задачи'
            )
        ],
        [
            KeyboardButton(
                text='Отписаться от бота'
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Для продолжения нажмите кнопку внизу'
)