from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
import json

from data.config import ADMINS
from keyboards.inline.managePost import confirmation_keyboard, post_callback, category_callback, category_keyboard
from loader import dp, bot
from states.newPost import NewPost


@dp.message_handler(Command("create_post"), chat_id=ADMINS)
async def create_post(message: Message):
    await message.answer("Chop etish uchun post yuboring. \n⚠️ Diqqat: Post faqat bitta rasmdan iborat bo'lsin va izohni rasm bilan birgalikda yuboring. Aks holda post yaroqli deb hisoblanmaydi.")
    await NewPost.NewMessage.set()

@dp.message_handler(state=NewPost.NewMessage, content_types=types.ContentTypes.ANY)
async def enter_message(message: Message, state: FSMContext):
    if message.content_type == 'photo':
        await state.update_data(file_id=message.photo[-1].file_id,text=message.caption, mention = message.from_user.get_mention())
    else:
        await state.update_data(text=message.html_text, mention = message.from_user.get_mention())
    await message.answer("Post chop etishga tayyor. Postni kimlarga ulashamiz ?", reply_markup=category_keyboard)
    await NewPost.next()

@dp.callback_query_handler(category_callback.filter(sending_type="groups") , state=NewPost.Category, user_id=ADMINS)
async def send_post_to_groups(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Yaxshi endi postni chop etish uchun tasdiqlang")
    await call.message.edit_reply_markup(reply_markup=confirmation_keyboard)
    await state.update_data(sending_type="groups")
    await NewPost.next()

@dp.callback_query_handler(category_callback.filter(sending_type="channels"), state=NewPost.Category,  user_id=ADMINS)
async def send_post_to_channels(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Yaxshi endi postni chop etish uchun tasdiqlang")
    await call.message.edit_reply_markup(reply_markup=confirmation_keyboard)
    await state.update_data(sending_type= "channels")
    await NewPost.next()
    
@dp.callback_query_handler(category_callback.filter(sending_type="users"), state=NewPost.Category, user_id=ADMINS)
async def send_post_to_users(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Yaxshi endi postni chop etish uchun tasdiqlang")
    await call.message.edit_reply_markup(reply_markup=confirmation_keyboard)
    await state.update_data(sending_type= "users")
    await NewPost.next()
        

@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm, user_id=ADMINS)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data.get('file_id'):
            file_id = data.get('file_id')
        text = data.get("text")
        mention = data.get("mention")
        sending_type = data.get("sending_type")
    await state.finish()
    await call.answer("Postni chop etishga ruxsat berdingiz.", show_alert=True)
    with open("data.json", "r") as f:
        acceptors = json.load(f)
    chats = acceptors[sending_type]["id"] or ADMINS
    for user in chats:
        if data.get('file_id'):
            await bot.send_photo(chat_id=user,photo=file_id, caption=text)
        else:
            await bot.send_message(chat_id=user, text=text)
    await call.message.edit_reply_markup()
    await call.message.edit_text("✅ Chop etildi ...")

@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm, user_id=ADMINS)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.answer("Postni chop etish bekor qilindi", show_alert=True)
    await call.message.edit_text(text="❌ Bekor qilindi")

@dp.message_handler(state=NewPost.Confirm, user_id=ADMINS)
async def unknown_post(message: Message):
    await message.answer("Chop etish yoki rad etishni tanlang")

@dp.message_handler(state=NewPost.Category, user_id=ADMINS)
async def unknown_post(message: Message):
    await message.answer("Kerakli guruhni tanlang.")