from aiogram import Bot, Dispatcher, F
from tg_utils.tg_handlers.start_handler import StartHandler
from configs.tg_config import token, admin_id
from aiogram.filters import Command
from tg_utils.tg_handlers import reg_handler, admin_handlers
from tg_utils.tg_states import user_reg_states

bot = Bot(token=token, parse_mode='HTML')
dispatcher = Dispatcher()


async def start_bot(bot: Bot):
    await bot.send_message(admin_id, text='Bot wos started!')


# dp.startup.register(start_bot)
# dp.message.register(handle_get_start, Command(commands='start'))
dispatcher.message.register(StartHandler, Command(commands='start'))
dispatcher.callback_query.register(admin_handlers.CheckLicManagerHandler, F.data == 'check_lic_man')

# хенделеры регистрации пользователей
# dp.message.register(reg_handler.start_register, F.text == 'start_registry')
dispatcher.callback_query.register(reg_handler.RegStartHandler, F.data == 'start_registry')
dispatcher.message.register(reg_handler.RegNameHandler, user_reg_states.RegisterState.regName)
dispatcher.message.register(reg_handler.RegPhoneHandler, user_reg_states.RegisterState.regPhone)