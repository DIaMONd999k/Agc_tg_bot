from abc import ABC, abstractmethod
import aiogram
from db_utils.tg_bot_db import tg_users


class BaseStartMessage(ABC):
    def __init__(self, user: tg_users.TgBotUser):
        self.user = user

    @abstractmethod
    def msg_start(self) -> str:
        raise NotImplemented


class UserStartMessage(BaseStartMessage):

    def msg_start(self) -> str:
        return (f'Добрый день, {self.user.user_full_name}!\n '
                f'Для продолжения работы выберите команду в меню!\n')


class AdminStartMessage(BaseStartMessage):
    def msg_start(self):
        return (f'Добрый день, {self.user.lastname} {self.user.fathername}!\n '
                f'Что я могу сделать для Вас?\n')


class NewUserStartMessage(BaseStartMessage):
    def msg_start(self):
        return (f'Добрый день, {self.user.user_full_name}!\n '
                f'Вас приветствует бот ООО "АвиагазЦентр"\n'
                f'Доступ к функционалу бота доступен только после регистрации!\n'
                f'Для регистрации нажмите кнопку ниже:\n')


class NotRegUserStartMessage(BaseStartMessage):
    def msg_start(self):
        return (f'Ваша заявка находится на рассмотрении у администратора!\n\n'
                f'Сообщение с результатом рассмотрения заявки будет направлено вам в этот чат!\n')


class NotImplementedStartMessage(BaseStartMessage):
    def msg_start(self):
        return (f'Извините!\n'
                f'Пока бот не доступен другим пользователям!')


def get_start_message(user: tg_users.TgBotUser) -> BaseStartMessage:
    if user:
        if user.isadmin:
            return AdminStartMessage(user)
    else:
        return NotImplementedStartMessage(user)

