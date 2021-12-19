import os
from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser 
from telethon.tl.functions.messages import ImportChatInviteRequest
import random # Imported random
import time



from dotenv import load_dotenv
load_dotenv()

api_id = os.environ.get("telegram_api_id")
api_hash = os.environ.get("telegram_api_hash")
phone_number = os.environ.get("phone_number") 
password = os.environ.get("telegram_password")

client = TelegramClient(f"anon", api_id, api_hash) # Created a sessions folder. Moved the session file into a folder called sessions
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
        time.sleep(1)
        await client.edit_message(event.message, "I've been naughty today")
        # await event.delete()
        print("Deleted message!")
        
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
    @client.on(events.NewMessage())
    async def handle_new_message(event):
        # print(event)
        # user = await event.get_sender()
        # print(user)
        group = await client.get_entity(649973711)
        await client.send_message(group, "Hello there group, this is an automated message")
            

    client.run_until_disconnected()

