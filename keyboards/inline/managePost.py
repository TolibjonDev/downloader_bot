from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

post_callback = CallbackData("create_post", "action")

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆗 Chop etish", callback_data=post_callback.new(action="post")),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=post_callback.new(action="cancel")),

        ]
    ]
)

category_callback = CallbackData("category", "sending_type")

category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [ InlineKeyboardButton(text="👥 Guruhlar", callback_data=category_callback.new(sending_type="groups")) ],
        [ InlineKeyboardButton(text="🌐 Kanallar", callback_data=category_callback.new(sending_type="channels")) ],
        [ InlineKeyboardButton(text="🤖 Bot Foydalanuvchilari", callback_data=category_callback.new(sending_type="users")) ],

    ]
)