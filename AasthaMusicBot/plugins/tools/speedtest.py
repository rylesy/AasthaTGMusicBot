#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
# A Powerful Music Bot Property Of Rocks Indian Largest Chatting Group

# Kanged By © @Dr_Asad_Ali
# Rocks © @Shayri_Music_Lovers
# Owner Asad Ali 
# Harshit Sharma
# All rights reserved. Yukki

import asyncio
import os

import speedtest
import wget
from pyrogram import filters

from strings import get_command
from AasthaMusicBot import app
from AasthaMusicBot.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("Running Download SpeedTest")
        test.download()
        m = m.edit("Running Upload SpeedTest")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("Sharing SpeedTest Results")
        path = wget.download(result["share"])
    except Exception as e:
        return m.edit(e)
    return result, path


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("Running Speed test")
    loop = asyncio.get_event_loop()
    result, path = await loop.run_in_executor(None, testspeed, m)
    output = f"""**sᴘᴇᴇᴅ ᴛᴇsᴛ ʀᴇsᴜʟᴛ ᴀᴛ** @Alexa_Help
    
<u>**ᴄʟɪᴇɴᴛ:**</u>
**ɪsᴘ:** {result['client']['isp']}
**ᴄᴏᴜɴᴛʀʏ:** {result['client']['country']}
  
<u>**sᴇʀᴠᴇʀ:**</u>
**ɴᴀᴍᴇ:** {result['server']['name']}
**ᴄᴏᴜɴᴛʀʏ:** {result['server']['country']}, {result['server']['cc']}
**sᴘᴏɴsᴇʀ:** {result['server']['sponsor']}
**ʟᴀᴛᴇɴᴄʏ:** {result['server']['latency']}  
**ᴘɪɴɢ:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
