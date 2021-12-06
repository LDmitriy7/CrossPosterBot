from aiogram import types

from loader import bot
from models import documents


async def send_edited_copy_of_msg(msg: types.Message, route: documents.Route):
    if msg.text:
        new_text = msg.text
        for replace in route.replaces:
            new_text = new_text.replace(replace.old_text, replace.new_text)

        await bot.send_message(route.target_id, new_text)
