from aiogram import types

import api
import commands
import config
import keyboards as kb
import texts
from loader import dp


@dp.message_handler(commands=commands.SHOW_ROUTES, user_id=config.Users.admins_ids)
async def show_first_route(msg: types.Message):
    routes = api.get_all_routes()
    index = 0

    if not routes:
        await msg.answer('There are no routes')
        return

    route = routes[index]
    route_info = texts.route_info.format(
        route_id=route.id,
        source_id=route.source_id,
        target_id=route.target_id,
    )

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

    route = routes[index]
    route_info = texts.route_info.format(
        route_id=route.id,
        source_id=route.source_id,
        target_id=route.target_id,
    )

    await query.message.edit_text(route_info, reply_markup=kb.FlipRoutes(index))

# @dp.message_handler(commands=commands.SHOW_ROUTES, user_id=config.Users.admins_ids)
# async def show_first_route(msg: types.Message):
#     routes = api.get_all_routes()
#
#     if not routes:
#         await msg.answer('There are no routes')
#         return
#
#     await msg.answer(routes[0].id)

# await msg.answer('Send me ID of <b>route</b>')

# @dp.message_handler(state=DelRouteConv.route_id)
# async def del_route_by_id(msg: types.Message, state: FSMContext):
#     try:
#         api.del_route(msg.text)
#     except api.RouteNotExists:
#         await msg.answer('Route does not exists')
#     else:
#         await state.finish()
#         await msg.answer(f'Route deleted')
