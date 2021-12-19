import os
from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser 
import random # Imported random
import time
# Library imports for stickers
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
from telethon.tl.types import InputStickerSetID

from dotenv import load_dotenv # pip install python-dotenv if your env variables are not loading

api_id = os.environ.get("telegram_api_id")
api_hash = os.environ.get("telegram_api_hash")
phone_number = os.environ.get("phone_number") 
password = os.environ.get("telegram_password")

client = TelegramClient(f"anon", api_id, api_hash) # Created a sessions folder. Moved the session file into a folder called sessions
client.start(phone_number, password)

# Added function
def generateRandomResponse():
    responses = [
        "Fill in whatever you want here",
        "It's better to write your own responses",
        "Minimum 3 responses, you can have more if you want!"
    ]
    random_index = random.randint(0, len(responses) - 1)
    return responses[random_index]


async def sendRandomSticker(to):
    sticker_sets = await client(GetAllStickersRequest(0))
    sticker_set_randnum = random.randint(0, len(sticker_sets.sets) - 1)
    sticker_set = sticker_sets.sets[sticker_set_randnum]
    stickers = await client(GetStickerSetRequest(
        stickerset=InputStickerSetID(
            id=sticker_set.id, 
            access_hash=sticker_set.access_hash
        )
    ))
    sticker_randnum = random.randint(0, len(stickers.documents) - 1)
    await client.send_file(to, stickers.documents[sticker_randnum])
    print("sent sticker")
    

if __name__ == '__main__':
    print('Program initiated')
    client.send_message("me", "Initiating program")

    @client.on(events.NewMessage(outgoing=True, pattern=r'.*(hell|heck|frick)')) # Add additional swear words if you want
    async def handle_swear(event):
        print(event)
        time.sleep(1)
        await client.edit_message(event.message, "I've been naughty today")
        # await event.delete()
        print("Deleted message!")

    @client.on(events.MessageRead())
    async def handle_read_message(event):
        time.sleep(1)
        if hasattr(event.original_update.peer, "user_id"):
            user = await client.get_entity(event.original_update.peer.user_id)
            # Change the first parameter if you want to send to someone else, maybe the user who read your message
            await client.send_message("me", f"I see you have read my message {user.first_name} {user.last_name}")
        else:
            print("Someone read my message from a group chat")
    
    @client.on(events.NewMessage(pattern=r'.*sticker')) # Sends a sticker whether you or someone else says sticker
    async def handle_sticker(event):
        user = await event.get_sender()
        await sendRandomSticker(user.username)

    @client.on(events.NewMessage(outgoing=True, pattern=r'\.save')) # Reply to someone with .save
    async def handle_message(event):
        if event.is_reply: # checks to see if sent message == .save
            replied = await event.get_reply_message()
            sender = replied.sender
            # Downloads the photo of the person you replied and stores the downloaded file's path in the variable: profile_path
            profile_path = await client.download_profile_photo(sender, f"images/{sender.username}.jpg") 
            # Uses the downloaded file and sends it back to the one you replied
            await client.send_file(sender, profile_path, caption="Your profile picture sucks")
            # await event.respond('Your profile picture suchs, {}'.format(sender.username))


    #additonal feature. Auto replying to group chat and replying to specifc message in groupchat
    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        message = generateRandomResponse()
        if event.is_private:     
            
            #ignore someone 
            # if event.message.peer_id.user_id != 41197530:
                #the reply to private chat
                if event.message.peer_id.user_id == 876675202: 
                    await client.send_message(event.message.peer_id,message=message)  # this works, send back to private chat

        #not private
        else:
                #check that it is a reply message
                if event.is_reply == True : 
                    print(event.original_update.chat_id) #the group id should be t he same as the below 
                    if event.original_update.chat_id ==  704140264: #the number should be the same as above 
                        await event.reply("wow")

                else:
                    #both replies back to the group chat
                    if event.message.peer_id.chat_id == 704140264:
                        await client.send_message(event.message.peer_id,message=message)
                        

                    if event.original_update.chat_id == 704140264:
                        await client.send_message(event.original_update.chat_id,message=message)
                        

    # # Additional features
    # @client.on(events.UserUpdate()) # Occurs whenever a user goes online or starts typing
    # async def handle_user_update(event):
    #     to = event.original_update.user_id
    #     user = await event.client.get_entity(to)
    #     print(event.user)
    #     if user.username == "Evolvedwukong":
    #         if event.typing:
    #             await client.send_message(user.username, "I see you typing!")
    #         else:
    #             await client.send_message(user.username, "I see you online!")


    client.run_until_disconnected()

