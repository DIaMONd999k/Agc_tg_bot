from abc import ABC, abstractmethod


class BaseCheckResultMessage(ABC):
    @abstractmethod
    def get_message(self, *args, **kwargs) -> str:
        raise NotImplemented


class CheckLicMangerMessage(BaseCheckResultMessage):
    def get_message(self, *args, **kwargs) -> str:
        if 'status_code' in kwargs:
            status_code = kwargs['status_code']
            if status_code == 200:
                return f'Менеждер лицензий работает без ошибок!'
            else:
                return f'Менеджер лицензий не работает, или работает с ошибками!'
        else:
            return f'Для получения текста сообщение пожалуйста передайте именованную переменную status_code!'


def get_messanger(action: str) -> BaseCheckResultMessage:
    if action == 'check_lic_man':
        return CheckLicMangerMessage()



