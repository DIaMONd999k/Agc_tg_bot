import asyncio

from aiogram import Bot
from utils.loggers import loggers
from db_utils.loodsman_db import loodsman_database
from utils.commands import set_commnds
from db_utils.tg_bot_db import tg_bot_database, tg_users
from configs import tg_bot_db_config, lood_db_config, tg_config, app_config
from app import tg_bot, tasker


async def start_tg_bot(bot: Bot) -> None:
    await set_commnds(bot=bot)
    try:
        loggers.tg_bot_logger.info('Bot was started!')
        await tg_bot.dispatcher.start_polling(bot)
    finally:
        loggers.tg_bot_logger.info('Bot was stopped!')
        await tg_bot.bot.session.close()


async def start_tasker(database: loodsman_database.LoodsmanDataBase,
                       tg_bot_users: tg_users.TgBotUsers,
                       polling_timeout: str,
                       bot: Bot) -> None:

    td = tasker.TaskDispatcher(database, tg_bot_users, polling_timeout, bot)
    try:
        loggers.td_logger.info('Task dispatcher was started!')
        await td.start_polling()
    except Exception as e:
        pass
    finally:
        pass


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()

    event_loop.create_task(start_tg_bot(tg_bot.bot))
    event_loop.create_task(start_tasker(app_config.lood_db,
                                        app_config.tg_bot_users,
                                        app_config.polling_timeout,
                                        tg_bot.bot))

    try:
        event_loop.run_forever()
    finally:
        event_loop.close()
