from typing import Optional, Union

import aiogram
import requests
from abc import ABC, abstractmethod
from aiogram.handlers import BaseHandler
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    ForceReply

from app import tg_bot

from tg_utils.tg_messages import admin_checks_msg
from configs.tg_config import lic_man_host


class BaseAdminCheckHandler(BaseHandler):
    def __init__(self, message: aiogram.types.Message, event):
        super().__init__(event=event)
        self.message: aiogram.types.Message = message
        self.messanger = admin_checks_msg.get_messanger(event)

    async def __call__(self) -> None:
        await self.handle()

    @abstractmethod
    async def handle(self) -> None:
        raise NotImplemented

    async def send_message(self, msg_text: str,
                           reply_markup: Optional[
                               Union[
                                   InlineKeyboardMarkup,
                                   ReplyKeyboardMarkup,
                                   ReplyKeyboardRemove,
                                   ForceReply
                               ]
                           ] = None,
                           protect_content: bool | None = True
                           ) -> None:
        if self.message.from_user.id != 1148015592:
            reply_markup = None
            protect_content = True
        match self.message:
            case Message():
                sender = self.message.answer
            case CallbackQuery():
                sender = self.message.message.answer
            case _:
                raise ValueError('the message type must be a aiogram.Message or aiogram.CallbackQuery only')
        await sender(msg_text,
                     reply_markup=reply_markup,
                     protect_content=protect_content)

    def _get_message_text(self, *args, **kwargs):
        return self.messanger.get_message(*args, **kwargs)

    async def answer(self,
                     reply_markup: Optional[
                         Union[
                             InlineKeyboardMarkup,
                             ReplyKeyboardMarkup,
                             ReplyKeyboardRemove,
                             ForceReply
                         ]
                     ] = None,
                     protect_content: bool | None = True,
                     *args, **kwargs) -> None:
        msg_text = self._get_message_text(*args, **kwargs)
        await self.send_message(msg_text, reply_markup, protect_content)


class CheckLicManagerHandler(BaseAdminCheckHandler):
    def __init__(self, message: aiogram.types.Message):
        event = 'check_lic_man'
        super().__init__(message, event)

    @staticmethod
    def _check_manager_status() -> int:
        try:
            response = requests.get(f'http://{lic_man_host}/api/get_manager_status/')
            status_code = response.status_code
        except requests.exceptions.ConnectionError:
            status_code = 500
        return status_code

    async def handle(self) -> None:
        status_code = self._check_manager_status()
        await self.answer(status_code=status_code)
