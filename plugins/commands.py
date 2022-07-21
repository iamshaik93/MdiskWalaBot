
from configs import START_MSG, ABOUT_HELP_TEXT, BOT_OWNER
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TeamTeleRoid.database import db


@Client.on_message(filters.command("help") & filters.private)
async def help_handler(_, event: Message):
    await event.reply_text(ABOUT_HELP_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Our Channel", url="https://t.me/iPopcornFlix"),
             InlineKeyboardButton("Our Group", url="https://t.me/iPopcornMovieGroup"),
             InlineKeyboardButton("About", callback_data="About_msg")]
        ])
    )

@Client.on_message(filters.command("total_users") & filters.private &  filters.chat(BOT_OWNER))
async def total_users(_, event: Message):
    total_users = await db.total_users_count()
    msg = f"""
    Users: {total_users} users

    """
    await event.reply_text(msg)
    

@Client.on_message( filters.command("start") & filters.private)
async def start_handler(_,event: Message):
    await event.reply_photo(
        photo='https://telegra.ph/file/3ff4dce771db4c22b0160.jpg',
        caption=START_MSG.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Our Channel", url="https://t.me/iPopcornFlix"),
             InlineKeyboardButton("Our Group", url="https://t.me/iPopcornMovieGroup")],

             [InlineKeyboardButton("About", callback_data="About_msg"),
             InlineKeyboardButton("Help", callback_data="Help_msg")
             ]
        ])
    )


