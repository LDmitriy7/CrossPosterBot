from aiogram import types

from loader import bot
from models import documents


async def send_edited_copy_of_msg(msg: types.Message, route: documents.Route):
    if msg.text:
        new_text = msg.html_text
        # for replace in route.replaces:
        #     new_text = new_text.replace(replace.old_text, replace.new_text)
        await bot.send_message(route.target_id, new_text, reply_markup=msg.reply_markup)
    elif msg.photo:
        new_caption = msg.html_text if msg.caption else None
        await bot.send_photo(route.target_id, msg.photo[-1].file_id, new_caption, reply_markup=msg.reply_markup)
