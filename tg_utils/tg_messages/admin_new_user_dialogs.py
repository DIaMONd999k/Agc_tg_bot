from abc import abstractmethod, ABC
from typing import Type

from aiogram.fsm.context import FSMContext
from tg_utils.tg_states.admin_reg_states import AdminRegisterState


class BaseMessage(ABC):
    def __init__(self, user: str | None = None) -> None:
        self.user = user

    @abstractmethod
    def get_message(self) -> str:
        raise NotImplemented


class MessageMultipleRequest(BaseMessage):
    def get_message(self) -> str:
        return (f'Найдено более одной заявки на регистрацию.\n'
                f'Выберите ФИО пользователя, которого необходимо добавить, из списка ниже:\n')


class MessageNewRequest(BaseMessage):
    def get_message(self) -> str:
        return (f'Новая заявка на регистрацию пользователя:\n'
                f'ФИО: {self.user.FullName}\n'
                f'Номер телефона: {self.user.phone}\n')


class MessageSearchUser(BaseMessage):
    def get_message(self) -> str:
        return (f'Выполнить поиск пользователя в БД Лоцман?\n'
                )


class MessageUserNotFound(BaseMessage):
    def get_message(self) -> str:
        return (f'Пользователь {self.user.FullName} не найден по ФИО в БД Лоцман.\n'
                f'Продолжить регистрацию вручную?\n')


class MessageUserFound(BaseMessage):
    def get_message(self) -> str:
        return (f'В Лоцмане найдено следующее совпадение:\n'
                f'{self.user.FullName}\n'
                f'Принять данного пользователя?\n')


class MessageSearchById(BaseMessage):
    def get_message(self) -> str:
        return (f'Ввести ID пользователя вручную?\n'
                )


class MessageInputIdManually(BaseMessage):
    def get_message(self) -> str:
        return f'Введите ID пользователя в БД Лоцман\n'


class MessageIdNotFound(BaseMessage):
    def get_message(self) -> str:
        return (f'Пользователь не найден.\n'
                f'Повторить попытку?\n'
                )


class MessageMultipleMatch(BaseMessage):
    def get_message(self) -> str:
        return (f'Найдено более одной заявки на регистрацию.\n'
                f'Выберите ФИО пользователя, которого необходимо добавить:\n'
                )


class MessageDeleteRequest(BaseMessage):
    def get_message(self) -> str:
        return (f'Удалить заявку?\n'
                )


async def get_new_user_message(state: FSMContext) -> Type[BaseMessage]:
    cur_state = await state.get_state()
    if cur_state == AdminRegisterState.multipleRequests.state:
        return MessageMultipleRequest
    elif cur_state == AdminRegisterState.searchInDB.state:
        return MessageSearchUser
    elif cur_state == AdminRegisterState.newUser.state:
        return MessageNewRequest
    elif cur_state == AdminRegisterState.userFound.state:
        return MessageUserFound
    elif cur_state == AdminRegisterState.userNotFound.state:
        return MessageUserNotFound
    elif cur_state == AdminRegisterState.searchById.state:
        return MessageSearchById
    elif cur_state == AdminRegisterState.idNotFound.state:
        return MessageIdNotFound
    elif cur_state == AdminRegisterState.requestId.state:
        return MessageInputIdManually
    elif cur_state == AdminRegisterState.multipleMatch.state:
        return MessageMultipleMatch
    elif cur_state == AdminRegisterState.deleteRequest.state:
        return MessageDeleteRequest
