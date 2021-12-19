import os # import os
from telethon.sync import TelegramClient, events

# Moving our secrets to a separate file called .env 
# Have to create a new file manually
api_id = os.environ.get("telegram_api_id")
api_hash = os.environ.get("telegram_api_hash")
phone_number = os.environ.get("phone_number") 

# Create the client and connect. Commented out the following 1 line
# use sequential_updates=True to respond to messages one at a time
client = TelegramClient(f"anon", api_id, api_hash, sequential_updates=True)
client.start(phone_number)

if __name__ == '__main__':
    print('Program initiated')
    client.send_message("me", "Initiating program")

    # Event handler. RUns code whenever a message is snet or received
    @client.on(events.NewMessage())
    async def handle_message(event):
        await client.send_message("me", "Hello myself!") # Make sure to await the send_message function!
        # await event.respond("Hello myself!!") # Another way to reply. Difference being it will automatically reply to the sender
        
        # Exploring Further
        # await client.send_message("Me", f"You messaged me on {event.message.date}")
        user = await event.get_sender()
        print(user)
        await client.send_message("Me", f"You are {user.first_name} {user.last_name} and you messaged me on {event.message.date}")
        
    client.run_until_disconnected()