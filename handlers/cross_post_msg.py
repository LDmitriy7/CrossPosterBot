from aiogram import types

import api
from loader import dp


@dp.message_handler()
@dp.channel_post_handler()
async def cross_post_msg(msg: types.Message):
    for route in api.get_routes_by_source(msg.chat.id):
        await api.send_edited_copy_of_msg(msg, route)
