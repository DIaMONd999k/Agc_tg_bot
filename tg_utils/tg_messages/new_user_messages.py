from abc import abstractmethod, ABC
from typing import Type, Union, Dict, Any

from aiogram.fsm.state import State as aiogramState
from tg_utils.tg_states.user_reg_states import RegisterState
from tg_utils.tg_messages import message_exception


class BaseMessage(ABC):
    def __init__(self,  reg_data: Union[Dict[str, Any], None]) -> None:
        self.reg_data = reg_data

    @abstractmethod
    def get_message(self) -> str:
        raise NotImplemented


class MessageRequestFio(BaseMessage):
    def get_message(self) -> str:
        return f'Пожалуйста укажите полностью ваши Фамилию Имя и Отчество:\n'


class MessageRequestPhone(BaseMessage):
    def get_message(self) -> str:
        return (f'Теперь, пожалуйста, укажите ваш номер телефона в формате:\n'
                '+7(xxx)xxx-xx-xx\n'
                'Или нажмите на кнопку "Отправить номер телефона"\n'
                'Это необходимо для предотвращения несанкционированного доступа к данным')


class MessageDataGotSuccess(BaseMessage):
    def get_message(self) -> str:
        return (f'Данные успешно получены\n'
                'Заявка на регистрацию направлена администратору\n')


class MessageWrongName(BaseMessage):
    def get_message(self) -> str:
        return (f'ФИО указаны в неправильном формате\n'
                'Укажите ФИО в формате:\n'
                'Фамилия Имя Отчество\n')


class MessageWrongPhone(BaseMessage):
    def get_message(self) -> str:
        return (f'Номер указан в неправильном формате\n'
                'Укажите номер в формате:\n'
                '+7(xxx)xxx-xx-xx\n')


class MessageRequestToAdmin(BaseMessage):
    def get_message(self) -> str:
        reg_name = self.reg_data.get('regname')
        reg_phone = self.reg_data.get('regphone')
        return (f'Поступила заявка на регистрацию\n' +
                f'ФИО: {reg_name}\n' +
                f'телефон: {reg_phone}\n')


def _get_messanger(state_for_message: aiogramState) -> Type[BaseMessage]:
    state = state_for_message.state
    match state:
        case RegisterState.requestFIO.state:
            return MessageRequestFio
        case RegisterState.regName.state:
            return MessageRequestFio
        case RegisterState.regPhone.state:
            return MessageRequestPhone
        case RegisterState.wrongName.state:
            return MessageWrongName
        case RegisterState.wrongPhone.state:
            return MessageWrongPhone
        case RegisterState.dataGotSuccess.state:
            return MessageDataGotSuccess
        case RegisterState.sendRequestToAdmin.state:
            return MessageRequestToAdmin
        case _:
            raise message_exception.CantGenerateMessage


def get_message(state_for_message: aiogramState, reg_data: Union[Dict[str, Any], None]) -> str:

    messanger = _get_messanger(state_for_message)
    return messanger(reg_data).get_message()

