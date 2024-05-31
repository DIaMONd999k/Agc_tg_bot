import asyncpg

from utils import singleton
from typing import Union


class LoodsmanUser:
    def __init__(self, record: Union[dict | asyncpg.Record]) -> None:
        match record:
            case dict() | asyncpg.Record():
                self._init_from_record(record)
            case _:
                raise TypeError('Данный тип записи задачи не поддерживается')

    def _init_from_record(self, record: Union[dict | asyncpg.Record]) -> None:
        try:
            self.id_actor: int = int(record['idactor'])
            self.user_full_name: str = str(record['userfullname'])
            self.main_role_name: str = str(record['mainrolename'])
        except Exception:
            raise TypeError('Данные для формирования задачи некорректны')


@singleton.singleton
class LoodsmanUsers:
    def __init__(self) -> None:
        self.users: list[LoodsmanUser] = []

    def add_users(self, recordset: Union[
                                        list[asyncpg.Record | dict],
                                        LoodsmanUser,
                                        asyncpg.Record
                                        ]) -> None:
        match recordset:
            case list():
                self._add_users_from_list(recordset)
            case asyncpg.Record() | dict():
                self._add_user_from_asyncpg_record(recordset)
            case LoodsmanUser():
                self._add_user(recordset)
            case _:
                raise TypeError("Данный тип списка задач не поддерживается")

    def _add_users_from_list(self, recordset: list) -> None:
        for record in recordset:
            match record:
                case asyncpg.Record():
                    self._add_user_from_asyncpg_record(record)
                case _:
                    raise TypeError("Данный тип записи задачи не поддерживается")

    def _add_user_from_asyncpg_record(self, record: asyncpg.Record) -> None:
        try:
            if not self._user_in_users(record['idactor']):
                self._add_user(LoodsmanUser(record))
        except Exception:
            raise TypeError("Данный тип записи задачи не поддерживается")

    def _add_user(self, task: LoodsmanUser) -> None:
        self.users.append(task)

    def __contains__(self, item: LoodsmanUser) -> bool:
        if isinstance(item, LoodsmanUser):
            return self._user_in_users(item.id_actor)

    def _user_in_users(self, id_actor: int) -> bool:
        for user in self.users:
            if id_actor == user.id_actor:
                return True
        return False
