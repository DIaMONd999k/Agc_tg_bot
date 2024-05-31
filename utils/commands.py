from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commnds(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='start'
        ),
        BotCommand(
            command='help',
            description='help'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())