from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import json
from data.config import ADMINS
from loader import dp,bot


# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     await message.answer(f"Salom, {message.from_user.full_name}!")


# Load existing data
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {
    "groups": {
        "id": [5944280734],
        "fullinfo": [
        {"fullname": "Saidkodirov \ud83c\uddf5\ud83c\uddf8", "id": 5944280734}
    ]
    }, 
    "channels": {
        "id": [5944280734],
        "fullinfo": [
        {"fullname": "Saidkodirov \ud83c\uddf5\ud83c\uddf8", "id": 5944280734}
    ]}, 
    "users": {
        "id": [5944280734],
        "fullinfo": [
            {"fullname": "Saidkodirov \ud83c\uddf5\ud83c\uddf8", "id": 5944280734},
        ]
    }
}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):

    await message.answer("Assalomu aleykum. Bu bot orqali youtube.com saytidagi videolarning musiqalarini yuklab olishingiz mumkin. Botdan foydalanish uchun video linkini botga yuboring.")

    # Add user ID to data
    if message.from_user.id not in data['users']['id']:
        data['users']["fullinfo"].append({
            "fullname": message.from_user.full_name,
            "id": message.from_user.id
        })
        data["users"]["id"].append(message.from_user.id)
        await bot.send_message(ADMINS[0], f"New user added to bot with chat id: <code>{message.from_user.id}</code>. {message.from_user.get_mention(as_html=True)}")

    # Save data
    with open('data.json', 'w') as f:
        json.dump(data, f)

@dp.message_handler(content_types=['new_chat_members'])
async def on_bot_added(message: types.Message):
    # Add group/channel ID to data
    chat_id = message.chat.id
    print(chat_id)
    print(message.chat.type)
    if message.chat.type == 'supergroup' or message.chat.type == 'group' and chat_id not in data['groups']["id"]:
        data['groups']["fullinfo"].append({
            "fullname": message.chat.full_name,
            "id": chat_id
        })
        data["groups"]["id"].append(chat_id)
        await bot.send_message(ADMINS[0], f"New Group added to bot with chat id: <code>{chat_id}</code>. {message.chat.full_name}")
    elif message.chat.type == 'channel' and chat_id not in data['channels']["id"]:
        data['channels']["fullinfo"].append({
            "fullname": message.chat.full_name,
            "id": chat_id
        })
        data["channels"]["id"].append(chat_id)
        await bot.send_message(ADMINS[0], f"New channel added to bot with chat id: <code>{chat_id}</code>. {message.chat.full_name}")
        

    # Save data
    with open('data.json', 'w') as f:
        json.dump(data, f)