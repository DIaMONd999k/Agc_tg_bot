import asyncio
import aiogram
import asyncpg

from asyncio import CancelledError
from contextlib import suppress
from typing import Any, AsyncGenerator, List
from db_utils.loodsman_db import loodsman_database, loodsman_tasks
from db_utils.tg_bot_db import tg_users, tg_bot_database
from utils import singleton
from utils.loggers import loggers


@singleton.singleton
class TaskDispatcher:
    def __init__(self,
                 database: loodsman_database.LoodsmanDataBase,
                 tg_users: tg_users.TgBotUsers,
                 polling_timeout: str,
                 bot: aiogram.Bot) -> None:
        self.database = database
        self.tg_users = tg_users
        self.polling_timeout: int = self.convert_pg_time_to_sec(polling_timeout)
        self.database.set_time_interval(polling_timeout)
        # self.loop = asyncio.get_running_loop()
        self.bot = bot
        self.tasks: loodsman_tasks.LoodsmanTasks = loodsman_tasks.LoodsmanTasks()

    @staticmethod
    def convert_pg_time_to_sec(timeinterval) -> int:
        __time, __time_unit = timeinterval.split(' ')
        __time = int(__time)
        match __time_unit:
            case 'microseconds':
                __time *= 10E-6
            case 'milliseconds':
                __time *= 10E-6
            case 'second':
                __time *= 1
            case 'minute':
                __time *= 60
            case 'hour':
                __time *= 3600
            case 'day':
                __time *= 3600*24
            case 'week':
                __time *= 3600*24*7
            case _:
                raise TypeError('Формат записи интервала проверки данных не соответствует требования PostreSQL')
        return __time

    async def check_tasks(self):
        pass

    @staticmethod
    def _generate_message(task: loodsman_tasks.LoodsmanTask, tg_user: tg_users.TgBotUser) -> str:
        message = f'Уважаемый {tg_user.lastname} {tg_user.fathername}!' + '\n'
        message = message + 'Вам поступило новое задание:' + '\n'
        message = message + 'id задачи: ' + str(task.id_stage) + '\n'
        message = message + 'Задание от пользователя: ' + task.bp_creator_fullname + '\n'
        message = message + 'Текст задания: ' + task.task + '\n'
        message = message + 'Наименование процесса: ' + task.b_proc_name + '\n'
        message = message + 'Дата выдачи: ' + str(task.task_send) + '\n\n'
        return message

    @staticmethod
    def _generate_log_message(task: loodsman_tasks.LoodsmanTask, tg_user: tg_users.TgBotUser) -> str:
        message = "INSERT INTO bot_data.task_history(idstage, tasksend, userid, bpcreatorfullname, task) "
        message += (f"VALUES({task.id_stage}, '{task.task_send}', "
                    f"{tg_user.userid}, '{task.bp_creator_fullname}', '{task.task}')")
        return message

    async def _send_task(self, task: loodsman_tasks.LoodsmanTask, tg_user: tg_users.TgBotUser) -> None:
        message = self._generate_message(task, tg_user)
        await self.bot.send_message(chat_id=tg_user.tgchatid, text=message)
        log_message = self._generate_log_message(task, tg_user)
        loggers.td_logger.info(log_message, extra={'action': 'send_message'})
        loggers.td_logger.debug(task.task)

    async def send_tasks(self, tasks: loodsman_tasks.LoodsmanTasks) -> None:
        for task in tasks.tasks:
            tg_user = self.tg_users.get_tg_user_by_lood_u_id(task.id_user)
            if tg_user is not None:
                await self._send_task(task, tg_user)

    async def _listen_tasks(
            self,
            polling_timeout: int,
    ) -> AsyncGenerator[list[asyncpg.Record], None]:

        failed = False
        while True:
            try:
                _tasks = await self.database.get_users_tasks()
            except Exception as e:
                failed = True
                loggers.td_logger.error("Failed to fetch updates - %s: %s", type(e).__name__, e)
                continue

            if failed:
                loggers.td_logger.info("Connection established")
                failed = False
            yield _tasks
            await asyncio.sleep(polling_timeout)

    async def _polling(
        self,
        polling_timeout: int,
    ) -> None:
        """
        Internal polling process

        :param:
        """

        loggers.td_logger.info(
            'Run polling'
        )
        try:
            async for task in self._listen_tasks(
                polling_timeout=polling_timeout
            ):
                self.tasks.add_tasks(task)
                if self.tasks.tasks:
                    await self.send_tasks(self.tasks)
        finally:
            loggers.td_logger.info("Polling was stopped")

    async def start_polling(self) -> None:
        """
        Polling runner

        :return:
        """
        loggers.td_logger.info("Start polling")
        try:
            tasks: List[asyncio.Task[Any]] = [asyncio.create_task(
                    self._polling(self.polling_timeout)
                )]
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in pending:
                # (mostly) Graceful shutdown unfinished tasks
                task.cancel()
                with suppress(CancelledError):
                    await task
            # Wait finished tasks to propagate unhandled exceptions
            await asyncio.gather(*done)

        finally:
            loggers.td_logger.info("Task dispatcher was stopped!")


