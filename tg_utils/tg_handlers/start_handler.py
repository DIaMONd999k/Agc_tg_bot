from abc import ABC, abstractmethod
import aiogram
from aiogram.handlers import BaseHandler
from configs.app_config import tg_bot_users, admin_chat_id

from tg_utils.tg_keyboards import admin_start_keyboards, kb_user_regisrter
from tg_utils.tg_messages import start_msg
from db_utils.tg_bot_db.tg_users import TgBotUser


class BaseStartHandler(BaseHandler):
    # bot: aiogram.Bot

    def __init__(self, message: aiogram.types.Message, event):
        super().__init__(event=event)
        self.message: aiogram.types.Message = message
        self.user = self.__get_user()
        self.messages = start_msg.get_start_message(self.user)

    async def __call__(self) -> None:
        await self.handle()

    def __get_user(self) -> TgBotUser| None:
        return tg_bot_users.get_tg_user_by_tg_chat_id(self.message.chat.id)

    @abstractmethod
    async def handle(self) -> None:
        raise NotImplemented


class StartHandler(BaseStartHandler):
    def __init__(self, message: aiogram.types.Message):
        event = 'start'
        super().__init__(message, event)

    async def handle(self) -> None:
        if self.message.from_user.id != admin_chat_id:
            reply_markup = [None]
            protect_content = True
        else:
            reply_markup = admin_start_keyboards.admin_start_keyboard,
            protect_content = True
        await self.message.answer(self.messages.msg_start(),
                                  reply_markup=reply_markup[0],
                                  protect_content=protect_content
                                  )


async def handle_get_start(message: aiogram.types.Message, bot: aiogram.Bot) -> None:
    await bot.send_message(
        message.from_user.id, f'Добрый день!\n' +
                              f'Вас приветствует Телеграмм Бот ООО "АвиагазЦентр"',
        reply_markup=kb_user_regisrter.register_keyboard,
        protect_content=True
    )


