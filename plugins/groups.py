import json
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from TeamTeleRoid.database import db
from configs import Config
import requests
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


# ##############################################################################################################
        
async def get_mdisk(link, api):
    url = 'https://diskuploader.mypowerdisk.com/v1/tp/cp'
    param = {'token': api, 'link': link
             }
    res = requests.post(url, json=param)
    try:
        shareLink = res.json()
        link = shareLink["sharelink"]
    except Exception as e:
        print(e)
    return link


async def replace_mdisk_link(text, api):
    links = re.findall(r'https?://mdisk.me[^\s]+', text)

    for link in links:
        mdisk_link = await get_mdisk(link, api)

        text = text.replace(link, mdisk_link)

    return text


async def group_link_convertor(group_id, text):
    api = await db.get_api_id(group_id)

    if api:
        answer = await replace_mdisk_link(text, api['api'])
    else:
        answer = text
    return answer

    
