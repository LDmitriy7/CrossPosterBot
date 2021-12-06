from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError

import api
import commands
import config
import texts
from loader import dp


class ChatNotResolved(Exception):
    def __init__(self, id_or_username: str):
        self.id_or_username = id_or_username


async def resolve_chat_id(id_or_username: str) -> int:
    try:
        chat = await dp.bot.get_chat(id_or_username)
        return chat.id
    except TelegramAPIError:
        raise ChatNotResolved(id_or_username)


@dp.message_handler(commands='test')
async def test(msg: types.Message):
    try:
        cid = await resolve_chat_id(msg.get_args())
        await msg.answer(f'Chat ID: {cid}')
    except ValueError as e:
        await msg.answer(f'Chat "{msg.get_args()}" not found')


@dp.message_handler(commands=commands.ADD_ROUTE, user_id=config.Users.admins_ids)
async def add_route(msg: types.Message):
    args = msg.get_args().split()

    if len(args) != 2:
        await msg.answer(texts.add_route_guide)
        return

    try:
        source_id, target_id = [await resolve_chat_id(a) for a in args]
    except ChatNotResolved as e:
        await msg.answer(f'Chat "{e.id_or_username}" not found')
        return

    route_id = api.add_route(source_id, target_id)
    await msg.answer(f'Route added\n\n(ID: <code>{route_id}</code>)')

#
# @dp.message_handler(commands=commands.DEL_ROUTE, user_id=config.Users.admins_ids)
# async def del_route(msg: types.Message):
#     try:
#         source_id, target_id = (int(i) for i in msg.get_args().split())
#     except ValueError:
#         await msg.answer(f'Use: /{commands.DEL_ROUTE} [source_id] [target_id]')
#         return
#
#     try:
#         api.del_route(source_id, target_id)
#     except api.RouteNotExists:
#         await msg.answer('Route does not exists')
#     else:
#         await msg.answer(f'Route deleted')
