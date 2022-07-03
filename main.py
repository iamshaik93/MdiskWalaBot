# (c) @RoyalKrrishna

from configs import Config
from pyrogram import Client, idle
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon import Button
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from TeamTeleRoid import group_link_convertor


tbot = TelegramClient('mdisktelethonbot', Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)
client = TelegramClient(StringSession( Config.USER_SESSION_STRING), Config.API_ID, Config.API_HASH)


async def get_user_join(id):
    ok = True
    try:
        await tbot(GetParticipantRequest(channel=int(Config.UPDATES_CHANNEL), participant=id))
        ok = True
    except UserNotParticipantError:
        ok = False
    return ok

@tbot.on(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
	await event.reply_photo("https://telegra.ph/file/f35d8b79281781574e6f4.jpg",
                         caption=Config.START_MSG.format(event.sender.first_name),
                         buttons=[
                             [Button.url("Our Channel", url="https://t.me/iPopcornFlix"),
                              Button.url("Our Group", url="https://t.me/iPopcornMovieGroup")],
                             [Button.inline("Help", "Help_msg"),
                              Button.inline("About", "About_msg")]])



@tbot.on(events.NewMessage(incoming=True))
async def message_handler(event):

    args = event.text

    if args.startswith("/"):
        return
    if await get_user_join(event.sender_id):
        pass
    else:
        haha = await event.reply(f'''**Hey! {event.sender.first_name} 😃**

**You Have To Join Our Update Channel To Use Me.**

**Click Bellow Button To Join Now.👇🏻**''', buttons=Button.url('🍿Updates Channel🍿', f'https://t.me/{Config.UPDATES_CHANNEL_USERNAME}'))
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        return await haha.delete()

    search = client.iter_messages(Config.CHANNEL_ID, limit=10, search=args)
    answer = f'**📂 {event.text}**\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n'
    c = 0
    async for msg in search:
        f_text = msg.text
        if "|||" in msg.text:
            f_text = msg.text.split("|||", 1)[0]
            msg_text = msg.text.html.split("|||", 1)[0]
        answer += f'**🍿 ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n' + '' + f_text.split("\n", 2)[
            -1] + ' **\n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n**Click Next For More Results 👇**'
        c += 1
        break
    finalsearch = []
    async for msg in search:
        finalsearch.append(msg)

    if c <= 0:
        answer = f'''**No Results Found For `{event.text}`❗️**

**Type Only Movie Name 💬**
**Check Spelling On** [𝗚𝗼𝗼𝗴𝗹𝗲](http://www.google.com/search?q={event.text.replace(' ', '%20')}%20Movie) 🔍
    '''
        buttons = None
        newbutton = [Button.url('Click To Check Spelling ✅',
                                f'http://www.google.com/search?q={event.text.replace(" ", "%20")}%20Movie')], [
                        Button.url('Click To Check Release Date 📅',
                                   f'http://www.google.com/search?q={event.text.replace(" ", "%20")}%20Movie%20Release%20Date')]
    else:
        buttons = [Button.inline('Next ➡️', f'1next_{args}')], [Button.inline(f'📑 Pages {1}/{len(finalsearch)}', 'pages')]
        newbutton = None
        pass
    
    
    if not event.is_private:
        answer = await group_link_convertor(event.chat_id, answer)

    image = None
    if buttons is None:
        result = await event.reply(answer, buttons=newbutton, link_preview=False)
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await event.delete()
        return await result.delete()
    if image is not None:
        try:
            result = await tbot.send_file(entity=event.chat_id, file=image, caption=answer, buttons=buttons,
                                          force_document=False)
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            await event.delete()
            return await result.delete()
        except:
            result = await event.reply(answer, buttons=buttons)
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            await event.delete()
            return await result.delete()
    else:
        result = await event.reply(answer, buttons=buttons)
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await event.delete()
        return await result.delete()


@tbot.on(events.CallbackQuery(func=lambda event: b"next_" in event.data))
async def movie_next(event):
    data = event.data.decode()
    index = int(data[:1])
    args = data[6:]
    search = client.iter_messages(Config.CHANNEL_ID, limit=10, search=args)
    finalsearch = []
    answer = f'**📂 {args}**\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n'

    async for msg in search:
        finalsearch.append(msg.text)
    try:
        f_text = finalsearch[index]
        if "|||" in f_text:
            f_text = f_text.split("|||", 1)[0]
        answer += f'**🍿 ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n' + '' + \
                  f_text.split("\n", 2)[
                      -1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nClick Next For More Results 👇**'
        buttons = [Button.inline('⬅️ Back', f'{index - 1}back_{args}'),
                   Button.inline('Next ➡️', f'{index + 1}next_{args}')], [Button.inline(f'📑 Pages {index + 1}/{len(finalsearch)}', 'pages')]
    except:
        answer = '**No More Results❗\n\nReason Is❓👇\n\n1 - Wrong Spelling 📌\n2 - Movie Not Released 📌\n3 - OTT, DVD Not Released 📌\n4 - Not Uploaded 📌\n\nType Correct Spelling ✅\nSearch In Google For Correct Name.🔍\n\nRequest Your Movie❗\n👉 @RoyalKrrishna**'
        buttons = [Button.inline('⬅️ Back', f'{index-1}back_{args}')], [Button.inline(f'📑 Pages {index}/{len(finalsearch)}', 'pages')]


    if not event.is_private:
        answer = await group_link_convertor(event.chat_id, answer)


    result = await event.edit(answer, buttons=buttons)
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await event.delete()
    return await result.delete()

@tbot.on(events.CallbackQuery(func=lambda event: b"back_" in event.data))
async def movie_back(event):
    data = event.data.decode()
    index = int(data[:1])
    args = data[6:]
    search = client.iter_messages(Config.CHANNEL_ID, limit=10, search=args)
    finalsearch = []
    answer = f'**📂 {args}**\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n'
    async for msg in search:
        finalsearch.append(msg.text)

    f_text = finalsearch[index]

    if "|||" in f_text:
        f_text = f_text.split("|||", 1)[0]
    answer += f'**🍿 ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n' + '' + \
              f_text.split("\n", 2)[
                  -1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nClick Next For More Results 👇**'
    if index == 0:
        buttons = [Button.inline('Next ➡️', f'{index + 1}next_{args}')], [Button.inline(f'📑 Pages {index+1}/{len(finalsearch)}', 'pages')]
    else:
        buttons = [Button.inline('⬅️ Back', f'{index - 1}back_{args}'),
                   Button.inline('Next ➡️', f'{index + 1}next_{args}')], [Button.inline(f'📑 Pages {index+1}/{len(finalsearch)}', 'pages')]
                   

    if not event.is_private:
        answer = await group_link_convertor(event.chat_id, answer)

    result = await event.edit(answer, buttons=buttons)
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await event.delete()
    return await result.delete()



# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)


print("Bot running...")
# Start Clients
Bot.start()
# User.start()
with tbot, client:
    tbot.run_until_disconnected()
    client.run_until_disconnected()

# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
# User.stop()
