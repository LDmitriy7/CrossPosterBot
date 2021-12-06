from aiogram import types

import api
import commands
import config
import keyboards as kb
from loader import dp


@dp.message_handler(commands=commands.SHOW_ROUTES, user_id=config.Users.admins_ids)
async def show_first_route(msg: types.Message):
    routes = api.get_all_routes()
    index = 0

    if not routes:
        await msg.answer('There are no routes')
        return

    route_info = await api.get_route_info(routes[index])
    await msg.answer(route_info, reply_markup=kb.FlipRoutes(index))


@dp.callback_query_handler(button=kb.FlipRoutes.FAKE_BUTTON)
async def fake_button(query: types.CallbackQuery):
    await query.answer('There are no routes')


@dp.callback_query_handler(button=kb.FlipRoutes.FLIP)
async def show_route_by_index(query: types.CallbackQuery, button: dict):
    routes = api.get_all_routes()
    index = int(button['index'])

    if index >= len(routes):
        await query.answer('There are no routes')
        return

    route_info = await api.get_route_info(routes[index])
    await query.message.edit_text(route_info, reply_markup=kb.FlipRoutes(index))
