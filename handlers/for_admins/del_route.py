from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import api
import commands
import config
from loader import dp


class DelRouteConv(StatesGroup):
    route_id = State()


@dp.message_handler(commands=commands.DEL_ROUTE, user_id=config.Users.admins_ids)
async def del_route_start(msg: types.Message):
    await DelRouteConv.first()
    await msg.answer('Send me ID of <b>route</b>')


@dp.message_handler(state=DelRouteConv.route_id)
async def del_route_by_id(msg: types.Message, state: FSMContext):
    try:
        api.del_route(msg.text)
    except api.RouteNotExists:
        await msg.answer('Route does not exists')
    else:
        await state.finish()
        await msg.answer(f'Route deleted')
