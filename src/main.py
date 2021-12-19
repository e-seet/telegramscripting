import os
from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser 
from telethon.tl.functions.messages import ImportChatInviteRequest
import random # Imported random
import time

from dotenv import load_dotenv

api_id = os.environ.get("telegram_api_id")
api_hash = os.environ.get("telegram_api_hash")
phone_number = os.environ.get("phone_number") 
password = os.environ.get("telegram_password")

client = TelegramClient(f"sessions/anon", api_id, api_hash) # Created a sessions folder. Moved the session file into a folder called sessions
client.start(phone_number, password)

# Added function
def generate_random_response():
    responses = [
        "Fill in whatever you want here",
        "It's better to write your own responses",
        "Minimum 3 responses, you can have more if you want!"
    ]
    random_index = random.randint(0, len(responses) - 1)
    return responses[random_index]

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


    #additonal feature. Auto replying to group chat and replying to specifc message in groupchat
    # @client.on(events.NewMessage(incoming=True))
    # async def handle_new_message(event):
    #     if event.is_private:     
            
    #         #ignore someone 
    #         # if event.message.peer_id.user_id != 41197530:
    #             #the reply to private chat
    #             if event.message.peer_id.user_id == 876675202: 
    #                 await client.send_message(event.message.peer_id,message="Hello")  # this works, send back to private chat

    #     #not private
    #     else:
    #             #check that it is a reply message
    #             if event.is_reply == True : 
    #                 print(event.original_update.chat_id) #the group id should be t he same as the below 
    #                 if event.original_update.chat_id ==  704140264: #the number should be the same as above 
    #                     await event.reply("wow")

    #             else:
    #                 #both replies back to the group chat
    #                 if event.message.peer_id.chat_id == 704140264:
    #                     await client.send_message(event.message.peer_id,message="Hi Group")  
                        

    #                 if event.original_update.chat_id == 704140264:
    #                     await client.send_message(event.original_update.chat_id,message="Hi Groups")  
                        


    client.run_until_disconnected()

