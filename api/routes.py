from __future__ import annotations

import mongoengine as me

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
