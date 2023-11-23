from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, IDFilter
from aiogram.dispatcher.filters import Command
import json
from data.config import ADMINS
from loader import dp,bot

@dp.message_handler(Command("users", prefixes="/:"), IDFilter(chat_id=ADMINS[0]))
async def show_bot_users(msg: types.Message):
        await msg.answer("salom Admin")
        with open('data.json', 'r') as f:
            data = json.load(f)
            users_count = len(data['users']['id'])
            gr_count = len(data['groups']['id'])
            ch_count = len(data['channels']['id'])
        with open("data.json", 'rb') as file:
            await msg.answer_document(document=file, caption=f"<b>All users id:</b>\n---------------\nUsers count: {users_count}\nGroups count: {gr_count}\nChannels count: {ch_count}")
            users_count = len(data['users'])
            gr_count = len(data['groups'])
            ch_count = len(data['channels'])
        with open("data.json", 'rb') as file:
            await msg.answer_document(document=file, caption=f"<b>All users id:</b>\n---------------\nUsers count: {users_count}\nGroups count: {gr_count}\nChannels count: {ch_count}")
