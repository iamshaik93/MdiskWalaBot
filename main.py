# (c) @RoyalKrrishna

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from TeamTeleRoid.forcesub import ForceSub
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon import Button
from tmdbv3api import TMDb, Movie, TV

# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
tstring = '1BVtsOHwBu0vHbseyZMPvHQjRPoX2tGphn3tuIt0XTlNd9jU36ozKw5Aec3Xxs81fzFq6sORCmehNMzEyQFyIwSVeyFx0sugnqQNmyGDs__HOgDPAc3k7BhW3PVfZmJ50QZecBmmo1S5RS1ubegIxNbtcLxfsDoxKb547rYxhHyEny7PPQHv1qOaNZwcBFZlhLcOZfV3FtlxJo4F2UChbgD7-43PFc0BgurLCLVB8lyX20R4InpNaDmi14n-lsFkti4Ep6FMAAuUYM49Ov-l1SgcNWjYLuzw66pJm6V7g2HWKeN9yqJ2LT_XBXzxP0ftnDw6F7qTF5-yOB1WccJLaEuWyCW6axEg='
tbot = TelegramClient('mdisktelethonbot', Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)
client = TelegramClient(StringSession(tstring), Config.API_ID, Config.API_HASH)
tmdb = TMDb()
tmdb.api_key = '8ebb221307122fc80aef95000840580b'
movie = Movie()
tv = TV()
# # User Client for Searching in Channel.
# User = Client(
#     session_name=Config.USER_SESSION_STRING,
#     api_id=Config.API_ID,
#     api_hash=Config.API_HASH
# )

@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
	await event.reply_photo("https://telegra.ph/file/165941ae764a56d6d9c89.jpg",
                                caption=Config.START_MSG.format(event.from_user.mention),
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton("Our Channel", url="https://t.me/iP_Movies"),
                                     InlineKeyboardButton("Our Group", url="https://t.me/iPopcornMovieGroup")],
                                    [InlineKeyboardButton("Help", callback_data="Help_msg"),
                                     InlineKeyboardButton("About", callback_data="About_msg")]]))

@Bot.on_message(filters.private & filters.command("help"))
async def help_handler(_, event: Message):

    await event.reply_text(Config.ABOUT_HELP_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Our Channel", url="https://t.me/iP_Movies"),
             InlineKeyboardButton("Our Group", url="https://t.me/iPopcornMovieGroup"), 
             InlineKeyboardButton("About", callback_data="About_msg")]
        ])
    )

@tbot.on(events.NewMessage(incoming=True))
async def test(event):
    args = event.text
    if '/start' in args or '/help' in args:
        return
    search = client.iter_messages(Config.CHANNEL_ID, limit=10, search=args)
    answer = f'**📂 Results For ➠ {event.text} \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n➠ Type Only Movie Name With Correct Spelling.✍️\n➠ Add Year For Better Result.🗓️\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    async for msg in search:
        f_text = msg.text
        if "|||" in msg.text:
            f_text = msg.text.split("|||", 1)[0]
            msg_text = msg.text.html.split("|||", 1)[0]
        answer += f'**🍿 Title ➠ ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n📜 About ➠ ' + '' + f_text.split("\n", 2)[-1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nAuto Delete In 5Min...⏰\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
        break
    buttons = [Button.inline('➡️ Next', f'1next_{args}')]
    try:
        image = f'http://image.tmdb.org/t/p/w500/{movie.search(args)[0].poster_path}'
    except:
        image = None
    if image is not None:
        try:
            result = await tbot.send_file(entity=event.chat_id, file=image, caption=answer, buttons=buttons, force_document=False)
        except:
            result = await event.reply(answer, buttons=buttons)
    else:
        result = await event.reply(answer, buttons=buttons)
    await asyncio.sleep(60)
    await result.delete()

@tbot.on(events.CallbackQuery(func=lambda event: b"next_" in event.data))
async def movie_next(event):
    data = event.data.decode()
    index = int(data[:1])
    args = data[6:]
    search = client.iter_messages(Config.CHANNEL_ID, limit=10, search=args)
    finalsearch = []
    answer = f'**📂 Results For ➠ {args} \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n➠ Type Only Movie Name With Correct Spelling.✍️\n➠ Add Year For Better Result.🗓️\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    async for msg in search:
        finalsearch.append(msg.text)
    try:
        f_text = finalsearch[index]
        if "|||" in f_text:
            f_text = f_text.split("|||", 1)[0]
        answer += f'**🍿 Title ➠ ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n📜 About ➠ ' + '' + \
                  f_text.split("\n", 2)[
                      -1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nAuto Delete In 5Min...⏰\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
        buttons = [Button.inline('⬅️ Back', f'{index - 1}back_{args}'),
                   Button.inline('➡️ Next', f'{index + 1}next_{args}')]
    except:
        answer = '❌ NO MORE RESULTS ❌'
        buttons = [Button.inline('⬅️ Back', f'{index - 1}back_{args}')]
    await event.edit(answer, buttons=buttons)

@tbot.on(events.CallbackQuery(func=lambda event: b"back_" in event.data))
async def movie_next(event):
    data = event.data.decode()
    index = int(data[:1])
    args = data[6:]
    search = client.iter_messages(Config.CHANNEL_ID, limit=10, search=args)
    finalsearch = []
    answer = f'**📂 Results For ➠ {args} \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n➠ Type Only Movie Name With Correct Spelling.✍️\n➠ Add Year For Better Result.🗓️\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    async for msg in search:
        finalsearch.append(msg.text)
    f_text = finalsearch[index]
    if "|||" in f_text:
        f_text = f_text.split("|||", 1)[0]
    answer += f'**🍿 Title ➠ ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n📜 About ➠ ' + '' + \
              f_text.split("\n", 2)[
                  -1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nAuto Delete In 60Sec...⏰\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    if index == 0:
        buttons = [Button.inline('➡️ Next', f'{index + 1}next_{args}')]
    else:
        buttons = [Button.inline('⬅️ Back', f'{index - 1}back_{args}'),
                   Button.inline('➡️ Next', f'{index + 1}next_{args}')]
    await event.edit(answer, buttons=buttons)



# @Bot.on_message(filters.incoming)
# async def inline_handlers(_, event: Message):
#     if event.text == '/start':
#         return
#     answers = f'**📂 Results For ➠ {event.text} \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n➠ Type Only Movie Name With Correct Spelling.✍️\n➠ Add Year For Better Result.🗓️\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
#     async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.text):
#         if message.text:
#             thumb = None
#             f_text = message.text
#             msg_text = message.text.html
#             if "|||" in message.text:
#                 f_text = message.text.split("|||", 1)[0]
#                 msg_text = message.text.html.split("|||", 1)[0]
#             answers += f'**🍿 Title ➠ ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n📜 About ➠ ' + '' + f_text.split("\n", 2)[-1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nAuto Delete In 5Min...⏰\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
#     try:
#         msg = await event.reply_text(answers)
#         await asyncio.sleep(60)
#         await event.delete()
#         await msg.delete()
#     except:
#         print(f"[{Config.BOT_SESSION_NAME}] - Failed to Answer - {event.from_user.first_name}")


@Bot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
        cb_data = cmd.data
        if "About_msg" in cb_data:
            await cmd.message.edit(
			text=Config.ABOUT_BOT_TEXT,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Our Channel", url="https://t.me/iP_Movies"),
						InlineKeyboardButton("Our Group", url="https://t.me/iPopcornMovieGroup")
					],
					[
						InlineKeyboardButton("Developer", url="https://t.me/RoyalKrrishna"),
						InlineKeyboardButton("Home", callback_data="gohome")
					]
				]
			),
			parse_mode="html"
		)
        elif "Help_msg" in cb_data:
            await cmd.message.edit(
			text=Config.ABOUT_HELP_TEXT,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("About", callback_data="About_msg"),
						InlineKeyboardButton("Our Channel", url="https://t.me/iP_Movies")
					], 
                                        [
						InlineKeyboardButton("Owner", url="https://t.me/RoyalKrrishna"),
						InlineKeyboardButton("Home", callback_data="gohome")
					]
				]
			),
			parse_mode="html"
		)
        elif "gohome" in cb_data:
            await cmd.message.edit(
			text=Config.START_MSG.format(cmd.from_user.mention),
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
                                        [
						InlineKeyboardButton("Help", callback_data="Help_msg"),
						InlineKeyboardButton("About", callback_data="About_msg")
					],
					[
						InlineKeyboardButton("Support", url="https://t.me/RoyalKrrishna"),
						InlineKeyboardButton("Channel", url="https://t.me/iP_Movies")
					]
				]
			),
			parse_mode="html"
		)

# Start Clients
Bot.start()
# User.start()
with tbot, client:
    client.run_until_disconnected()
    tbot.run_until_disconnected()

# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
# User.stop()
