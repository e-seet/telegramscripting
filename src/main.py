import os
from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser 
import random # Imported random

api_id = os.environ.get("telegram_api_id")
api_hash = os.environ.get("telegram_api_hash")
phone_number = os.environ.get("phone_number") 

client = TelegramClient(f"sessions/anon", api_id, api_hash, sequential_updates=True) # Created a sessions folder. Moved the session file into a folder called sessions
client.start(phone_number)

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


    @client.on(events.NewMessage())
    async def handle_message(event):
        await event.respond(generate_random_response())
        
    client.run_until_disconnected()



