import asyncio
from abc import abstractmethod
from typing import Optional, Union, Dict, Any

import aiogram.types
from aiogram.handlers import BaseHandler
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    ForceReply
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State as aiogramState
from app import tg_bot
from tg_utils.tg_states.user_reg_states import RegisterState
from utils.validators import validators_reg_handlers
from configs.tg_config import admin_id
from tg_utils.tg_messages import new_user_messages
from tg_utils.tg_keyboards import kb_user_regisrter


class BaseRegHandler(BaseHandler):
    def __init__(self, message: Message | CallbackQuery, state: FSMContext) -> None:
        self.event = asyncio.get_running_loop().create_task(state.get_state())
        super().__init__(event=self.event)
        self.state = state
        self.message = message
        self.reg_data: Union[Dict[str, Any], None] = None
        self.message_text: str | None = None

    async def __call__(self) -> None:
        await self.handle()

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
        match self.message:
            case Message():
                await self.message.answer(msg_text,
                                          reply_markup=reply_markup,
                                          protect_content=protect_content)
            case CallbackQuery():
                await self.message.message.answer(msg_text,
                                                  reply_markup=reply_markup,
                                                  protect_content=protect_content
                                                  )
            case _:
                raise ValueError('the message type must be a aiogram.Message or aiogram.CallbackQuery only')

    def _get_message_text(self, state_for_message):
        return new_user_messages.get_message(state_for_message, self.reg_data)

    async def answer(self, state_for_message: aiogramState,
                     reply_markup: Optional[
                         Union[
                             InlineKeyboardMarkup,
                             ReplyKeyboardMarkup,
                             ReplyKeyboardRemove,
                             ForceReply
                         ]
                     ] = None,
                     protect_content: bool | None = True) -> None:
        msg_text = self._get_message_text(state_for_message)
        await self.send_message(msg_text, reply_markup, protect_content)

    def _get_text_from_message(self) -> str:
        match self.message:
            case aiogram.types.message.Message():
                return self.message.text
            case aiogram.types.callback_query.CallbackQuery():
                return self.message.message.text

    @abstractmethod
    async def handle(self) -> None:
        raise NotImplemented


class RegStartHandler(BaseRegHandler):
    """Ловим начало регистрации и запрашиваем фамилию"""

    def __init__(self, message: Message | CallbackQuery, state: FSMContext) -> None:
        super().__init__(message, state)
        self.current_state = RegisterState.requestFIO
        self.next_state: aiogramState = RegisterState.regName

    async def handle(self) -> None:
        await self.state.set_state(self.current_state)
        await self.message.message.edit_reply_markup(reply_markup=None)
        await self.answer(self.current_state)
        await self.state.set_state(self.next_state)


class RegNameHandler(BaseRegHandler):
    """Ловим фимилию, проверяем ее и если всё хорошо запрашиваем телефон"""

    def __init__(self, message: Message | CallbackQuery, state: FSMContext) -> None:
        super().__init__(message, state)
        self.cur_state: aiogramState = RegisterState.regName
        self.next_state: aiogramState = RegisterState.regPhone
        self.err_state: aiogramState = RegisterState.wrongName

    async def handle(self) -> None:
        self.message_text = self._get_text_from_message()
        if validators_reg_handlers.validate_fio(self.message_text):
            await self.state.update_data(regname=self.message_text)
            await self.state.set_state(RegisterState.regPhone)
            await self.answer(self.next_state, reply_markup=kb_user_regisrter.request_phone_keyboard)

        else:
            self.next_state: aiogramState = RegisterState.regName
            await self.state.set_state(self.next_state)
            await self.answer(self.err_state)


class RegPhoneHandler(BaseRegHandler):
    """Ловим телефон, проверяем его и если всё хорошо запрашиваем отправляем на регистрацию"""

    def __init__(self, message: Message | CallbackQuery, state: FSMContext) -> None:
        super().__init__(message, state)
        self.cur_state: aiogramState = RegisterState.regPhone
        self.next_state: aiogramState = RegisterState.dataGotSuccess
        self.err_state: aiogramState = RegisterState.wrongPhone

    def _get_phone_from_message(self) -> str | None:
        if self.message.contact is not None:
            return self.message.contact.phone_number
        else:
            message_text = self._get_text_from_message()
            if not validators_reg_handlers.validate_phone(message_text):
                return None
            else:
                return message_text

    async def finish_registration(self, phone_number: str) -> None:
        await self.state.update_data(regphone=phone_number)
        self.reg_data = await self.state.get_data()
        await self.answer(self.next_state)
        msg_text = self._get_message_text(RegisterState.sendRequestToAdmin)
        await tg_bot.bot.send_message(admin_id, msg_text)
        await self.state.clear()

    async def handle(self) -> None:
        phone_number = self._get_phone_from_message()
        if phone_number is not None:
            await self.finish_registration(phone_number)
        else:
            await self.state.set_state(RegisterState.wrongPhone)
            await self.answer(self.err_state, reply_markup=kb_user_regisrter.request_phone_keyboard)
