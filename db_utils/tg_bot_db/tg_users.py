from dataclasses import dataclass

import asyncpg

from typing import Union
from utils import singleton


@dataclass
class URole:
    roleid: int
    rolename: str


@dataclass
class UGroup:
    groupid: int
    groupname: str


class TgBotUser:
    def __init__(self, records: list[asyncpg.Record]) -> None:
        self.userid: int
        self.tgchatid: int
        self.idactor: int
        self.firstname: str | None = None
        self.lastname: str | None = None
        self.fathername: str | None = None
        self.isadmin: bool = False
        self.roles: list[URole] = []
        self.groups: list[UGroup] = []
        self._set_data_from_list_of_records(records)

    def _set_data_from_list_of_records(self, records: list[asyncpg.Record]) -> None:
        try:
            self.userid = int(records[0]['userid'])
            self.tgchatid = int(records[0]['tgchatid'])
            self.idactor = int(records[0]['idactor'])
            self.firstname = str(records[0]['firstname'])
            self.lastname = str(records[0]['lastname'])
            self.fathername = str(records[0]['fathername'])
            for record in records:
                if not self.isadmin:
                    if bool(record['isadmin']):
                        self.isadmin = bool(record['isadmin'])
                if int(record['groupid']) != 0:
                    self.append_group(int(record['groupid']), str(record['groupname']))
                if int(record['roleid']) != 0:
                    self.append_role(int(record['roleid']), str(record['rolename']))
        except Exception:
            raise TypeError('Данные для формирования пользователя некорректны')

    def append_role(self, roleid: int, rolename: str) -> None:
        for role in self.roles:
            if roleid == role.roleid:
                break
        else:
            self.roles.append(URole(roleid, rolename))

    def append_group(self, groupid: int, groupname: str) -> None:
        for group in self.groups:
            if groupid == group.groupid:
                break
        else:
            self.groups.append(UGroup(groupid, groupname))

    @property
    def user_full_name(self) -> str:
        if self.firstname is not None and self.lastname is not None:
            if self.fathername is not None:
                return f'{self.lastname} {self.firstname} {self.fathername}'
            else:
                return f'{self.lastname} {self.firstname}'
        else:
            return ''


@singleton.singleton
class TgBotUsers:
    def __init__(self) -> None:
        self.users: list[TgBotUser] = []

    def add_users(self, recordset: Union[
                                        list[asyncpg.Record],
                                        TgBotUser,
                                        asyncpg.Record
                                        ]) -> None:
        match recordset:
            case list():
                recordset = self.__del_existing_users_from_list(recordset)
                self._add_users_from_list(recordset)
            case asyncpg.Record():
                self._add_user_from_asyncpg_record(recordset)
            case TgBotUser():
                self.__append_user(recordset)
            case _:
                raise TypeError("Данный тип списка задач не поддерживается")

    def _add_users_from_list(self, list_of_recordset: list[asyncpg.Record]) -> None:
        if len(list_of_recordset) != 0:
            if len(list_of_recordset) == 1:
                self.__append_user(TgBotUser(list_of_recordset))
            else:
                __user_id = int(list_of_recordset[0]['userid'])
                __user_data_list: list[asyncpg.Record] = [list_of_recordset[0]]
                for record in list_of_recordset[1:]:
                    if record['userid'] == __user_id:
                        __user_data_list.append(record)
                    else:
                        self.__append_user(TgBotUser(list(record)))
                        __user_id = record['userid']
                        __user_data_list.clear()
                        __user_data_list.append(record)
                self.users.append(TgBotUser(__user_data_list))
                __user_data_list.clear()
        else:
            raise TypeError("Данный тип записи задачи не поддерживается")

    def __del_existing_users_from_list(self, list_of_recordset: list[asyncpg.Record]) -> list[asyncpg.Record]:
        for record in list_of_recordset:
            if self._user_in_users(record['userid']):
                list_of_recordset.remove(record)
        return list_of_recordset

    def _add_user_from_asyncpg_record(self, record: asyncpg.Record) -> None:
        try:
            if not self._user_in_users(record['userid']):
                self.__append_user(TgBotUser(list(record)))
        except Exception:
            raise TypeError("Данный тип записи задачи не поддерживается")

    def __append_user(self, user: TgBotUser) -> None:
        self.users.append(user)

    def __contains__(self, item: TgBotUser) -> bool:
        if isinstance(item, TgBotUser):
            return self._user_in_users(item.userid)

    def _user_in_users(self, userid: int) -> bool:
        for user in self.users:
            if userid == user.userid:
                return True
        return False

    def get_tg_user_by_lood_u_id(self, loodsman_u_id: int) -> TgBotUser | None:
        for user in self.users:
            if loodsman_u_id == user.idactor:
                return user
        return None

    def get_tg_user_by_tg_chat_id(self, tg_chat_id) -> TgBotUser | None:
        for user in self.users:
            if tg_chat_id == user.tgchatid:
                return user
        return None
