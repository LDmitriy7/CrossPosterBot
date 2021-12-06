from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import TelegramAPIError
from aiogram_utils.storage_proxy import StorageProxy

import api
import commands
import config
from loader import dp
from models import documents


class AddRouteConv(StatesGroup):
    source_id = State()
    target_id = State()


class ChatNotResolved(Exception):
    def __init__(self, id_or_username: str):
        self.id_or_username = id_or_username


async def resolve_chat_id(id_or_username: str) -> int:
    try:
        chat = await dp.bot.get_chat(id_or_username)
        return chat.id
    except TelegramAPIError:
        raise ChatNotResolved(id_or_username)


@dp.message_handler(commands=commands.ADD_ROUTE, user_id=config.Users.admins_ids)
async def add_route_start(msg: types.Message):
    await AddRouteConv.first()
    await msg.answer('Send me ID of <b>source</b> (you can use usernames for channels and supergroups)')


@dp.message_handler(state=AddRouteConv.source_id)
async def add_route_source(msg: types.Message):
    try:
        source_id = await resolve_chat_id(msg.text)
    except ChatNotResolved as e:
        await msg.answer(f'Chat "{e.id_or_username}" not found')
        return

    async with StorageProxy(documents.Route) as route:
        route.source_id = source_id

    await AddRouteConv.next()
    await msg.answer('Send me ID of <b>target</b> (you can use usernames for channels and supergroups)')


@dp.message_handler(state=AddRouteConv.target_id)
async def add_route_target(msg: types.Message, state: FSMContext):
    try:
        target_id = await resolve_chat_id(msg.text)
    except ChatNotResolved as e:
        await msg.answer(f'Chat "{e.id_or_username}" not found')
        return

    async with StorageProxy(documents.Route) as route:
        route.target_id = target_id

    route.save()
    route_info = await api.get_route_info(route)

    await state.finish()
    await msg.answer(route_info)
