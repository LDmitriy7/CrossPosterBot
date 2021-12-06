from __future__ import annotations

import mongoengine as me
from aiogram.utils.exceptions import TelegramAPIError

import texts
from loader import bot
from models import documents


class RouteNotExists(Exception):
    pass


# def add_route(source_id: int, target_id: int) -> str:
#     """Return id of new route."""
#     route = documents.Route(source_id=source_id, target_id=target_id).save()
#     return str(route.id)


def del_route(route_id: str):
    """Delete route or raise exception."""
    try:
        route = documents.Route.objects(id=route_id).first()
    except me.errors.ValidationError:
        raise RouteNotExists()

    if route:
        route.delete()
    else:
        raise RouteNotExists()


def get_all_routes() -> list[documents.Route]:
    return [r for r in documents.Route.objects()]


def get_routes_by_source(source_id: int) -> list[documents.Route]:
    return [route for route in documents.Route.objects(source_id=source_id)]


async def get_route_info(route: documents.Route) -> str:
    try:
        source_chat = await bot.get_chat(route.source_id)
        source_url = await source_chat.get_url()
        source_name = f'<a href="{source_url}">{source_chat.full_name}</a>'
    except TelegramAPIError:
        source_name = texts.chat_not_found

    try:
        target_chat = await bot.get_chat(route.target_id)
        target_url = await target_chat.get_url()
        target_name = f'<a href="{target_url}">{target_chat.full_name}</a>'
    except TelegramAPIError:
        target_name = texts.chat_not_found

    return texts.route_info.format(
        route_id=route.id,
        source_id=route.source_id,
        source_name=source_name,
        target_id=route.target_id,
        target_name=target_name,
    )
