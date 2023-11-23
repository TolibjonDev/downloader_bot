from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Regexp
import json
from pytube import YouTube
from data.config import ADMINS
from loader import dp,bot
import re
from io import BytesIO


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    if re.match(youtube_regex, message.text):
        link = message.text
        buffer = BytesIO()
        yt = YouTube(link)
        if yt.check_availability() is None:
            yt_audio = yt.streams.get_audio_only()
            yt_audio.download(f"{message.from_user.id}", f"{yt.title}_{message.from_user.full_name}.mp4")
            yt_audio.stream_to_buffer(buffer=buffer)

            await message.answer_chat_action(action=types.ChatActions.UPLOAD_AUDIO)
            title = yt.title
            channel = yt.channel_url
            author = yt.author
            caption = f"<b>ℹ️ Nomi</b>: {title}\n"
            caption += f"<b>📹 Youtube kanal:</b> <a href='{channel}'>{author}</a>\n"
            caption += "--------------------------\n"
            caption += f"<b>👨🏻‍💻 Admin:</b> @Saidkodirov"
            buffer.seek(0)
            await message.answer_audio(audio=buffer, caption=caption)
            await bot.send_message(chat_id=ADMINS[0], text=f"<i>{message.text}</i> ni {message.from_user.full_name} {message.from_user.get_mention(as_html=True)} yubormoqda. ")
            await message.delete()
    
    else:
        await message.answer("Siz youtube link yubormayabsiz...")
        await bot.send_message(chat_id=ADMINS[0], text=f"<i>{message.text}</i> ni {message.from_user.full_name} {message.from_user.get_mention(as_html=True)} yubormoqda. ")
