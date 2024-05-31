import asyncpg
import datetime

from typing import Dict, Any, Union
from utils import singleton


class LoodsmanTask:
    def __init__(self, record: Union[dict | asyncpg.Record]) -> None:
        match record:
            case dict() | asyncpg.Record():
                self._init_from_record(record)
            case _:
                raise TypeError('Данный тип записи задачи не поддерживается')

    def _init_from_record(self, record: Union[dict | asyncpg.Record]) -> None:
        try:
            self.id_stage: int = int(record['idstage'])
            self.id_b_proc: int = int(record['idbproc'])
            self.b_proc_name: str = record['bprocname']
            self.id_user: int = int(record['iduser'])
            self.user_full_name: str = str(record['userfullname'])
            self.bp_creator_fullname:  str = str(record['bpcreatorfullname'])
            self.task: str = str(record['task'])
            self.task_send: datetime.datetime = record['tasksend']
        except Exception:
            raise TypeError('Данные для формирования задачи некорректны')

    def __eq__(self, other):
        return True if other.id_stage == self.id_stage else False


@singleton.singleton
class LoodsmanTasks:
    def __init__(self) -> None:
        self.tasks: list[LoodsmanTask] = []

    def add_tasks(self, recordset: Union[
                                        list[asyncpg.Record | dict],
                                        LoodsmanTask,
                                        asyncpg.Record
                                        ]) -> None:
        _old_tasks = self.tasks.copy()
        match recordset:
            case list():
                self._add_tasks_from_list(recordset)
            case asyncpg.Record() | dict():
                self._add_task_from_asyncpg_record(recordset)
            case LoodsmanTask():
                self._add_task(recordset)
            case _:
                raise TypeError("Данный тип списка задач не поддерживается")
        if _old_tasks:
            self._del_old_tasks(_old_tasks)

    def _del_old_tasks(self, _old_tasks) -> None:
        if self.tasks:
            for task in _old_tasks:
                self.tasks.remove(task)
        _old_tasks.clear()

    def _add_tasks_from_list(self, recordset: list) -> None:
        for record in recordset:
            match record:
                case asyncpg.Record():
                    self._add_task_from_asyncpg_record(record)
                case _:
                    raise TypeError("Данный тип записи задачи не поддерживается")

    def _add_task_from_asyncpg_record(self, record: asyncpg.Record) -> None:
        try:
            if not self._task_in_tasks(record['idstage']):
                self._add_task(LoodsmanTask(record))
        except Exception:
            raise TypeError("Данный тип записи задачи не поддерживается")

    def _add_task(self, task: LoodsmanTask) -> None:
        self.tasks.append(task)

    def __contains__(self, item: LoodsmanTask) -> bool:
        if isinstance(item, LoodsmanTask):
            return self._task_in_tasks(item.id_stage)

    def _task_in_tasks(self, id_stage: int) -> bool:
        for task in self.tasks:
            if id_stage == task.id_stage:
                return True
        return False
