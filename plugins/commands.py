
from configs import Config
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TeamTeleRoid.database import db


@Client.on_message(filters.private & filters.command("help"))
async def help_handler(_, event: Message):
    await event.reply_text(Config.ABOUT_HELP_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Our Channel", url="https://t.me/iPopcornFlix"),
             InlineKeyboardButton("Our Group", url="https://t.me/iPopcornMovieGroup"),
             InlineKeyboardButton("About", callback_data="About_msg")]
        ])
    )

@Client.on_message(filters.private & filters.command("total_users") & filters.chat(Config.BOT_OWNER))
async def total_users(_, event: Message):
    total_users = db.total_users_count()
    msg = f"""
    Users: {total_users}

    """
    await event.reply_text(msg)
    

