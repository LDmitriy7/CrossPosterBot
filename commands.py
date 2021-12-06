from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError

import config
from loader import dp

START = 'start'
CANCEL = 'cancel'
BROADCAST = 'broadcast'
ADD_ROUTE = 'add_route'
DEL_ROUTE = 'del_route'
SHOW_ROUTES = 'show_routes'

USER_COMMANDS = [
    types.BotCommand(START, 'Start bot'),
    types.BotCommand(CANCEL, 'Cancel'),
]

ADMIN_COMMANDS = USER_COMMANDS + [
    # types.BotCommand(BROADCAST, 'Рассылка'),
    types.BotCommand(ADD_ROUTE, 'Add route'),
    types.BotCommand(DEL_ROUTE, 'Delete route'),
    types.BotCommand(SHOW_ROUTES, 'Show routes'),
]


async def setup():
    await dp.bot.set_my_commands(USER_COMMANDS)

    for user_id in config.Users.admins_ids:
        with suppress(TelegramAPIError):
            await dp.bot.set_my_commands(ADMIN_COMMANDS, scope=types.BotCommandScopeChat(user_id))
