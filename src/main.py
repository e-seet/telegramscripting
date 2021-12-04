import time
from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
import urllib.request
import os
import random

from dotenv import load_dotenv
load_dotenv()




api_id = os.environ.get("telegram_api_id")
api_hash =os.environ.get("telegram_api_hash")
phone = os.environ.get("telegram_phone_number")
session_file = os.environ.get("telegram_session_file") #this is the username. It also creates a session file so we do not always need to key in the 2fa
#optional
password = os.environ.get("telegram_password")

def checkEnvironment():
    print(api_hash)
    print(phone)
    print(api_id)

checkEnvironment()


#file =  "C:\\Users\\eddie\\Desktop\\telegram coding\\"



def generate_random_response():
    responses = [
        "Hi there, sorry, but I'm away now. Please contact me later",
        "Another time, I'm a busy man",
        "Anything urgent, please call instead",
    ]
    index = random.randint(0, len(responses) - 1)
    
    return responses[index]

#Auto-reply message
me = "me"

# # Create the client and connect. Commented out the following 1 line
# # use sequential_updates=True to respond to messages one at a time
client = TelegramClient(f"sessions/anon", api_id, api_hash, sequential_updates=True)

client.start(phone, password)

client.send_message(me, "Initiating program")

async def sendRandomSticker():
    sticker_sets = await client(GetAllStickersRequest(0))
    sticker_set_randnum = random.randint(0, len(sticker_sets.sets))
    sticker_set = sticker_sets.sets[sticker_set_randnum]
    stickers = await client(GetStickerSetRequest(
        stickerset=InputStickerSetID(
            id=sticker_set.id, 
            access_hash=sticker_set.access_hash
        )
    ))
    sticker_randnum = random.randint(0, len(stickers.documents))
    await client.send_file("me", stickers.documents[sticker_randnum])

if __name__ == '__main__':
    # Triggers on any message, even when messaging yourself
    @client.on(events.NewMessage())
    async def handle_message(event):
        print("Got your message")
        print(event.from_id)
        await sendRandomSticker()

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        if event.is_private:  # only auto-reply to private chats
            _from = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
            print(f"From: {_from}")
            if not _from.bot:  # skip auto-reply to bots
                print(time.asctime(), '-', event.message)  # optionally log time and message
                time.sleep(1)  # pause for 1 second to rate-limit automatic replies

                #if this particular person messages me.
                if "detonate" in event.message.raw_text:
                    await event.respond(me, "Detonating explosives. Countdown starting")
                    for i in range(5, 0, -1):
                        await event.respond(me, str(i) + "...")
                        time.sleep(1)
                    await event.respond(me, "That was a joke.")
                #if anyone elses.
                else:                
                    #spamm the poor guy anyways. :P !Note: the first parameter for this is the telegram handler
                    # await client.send_file('EvolvedApeShit', getgif())
                    #replies back to the original event with the message declared earlier.
                    response = generate_random_response()
                    print(time.asctime(), response)  # log time and message to see how fast the program is running.
                    print("")
                    await event.respond(response)


    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone, password)
        
    # client.loop.run_until_complete(main())
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')



