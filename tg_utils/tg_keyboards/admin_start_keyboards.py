from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_lic_man_button = InlineKeyboardButton(
    text='Проверить менеджер лицензий',
    callback_data='check_lic_man'
                )

not_implemented_button = InlineKeyboardButton(
    text='Кнопка для вида',
    callback_data='nothing'
                )

admin_start_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
                    [check_lic_man_button, not_implemented_button]
]
                )
