import os
from telethon.sync import TelegramClient

# Input the following information
# You can retrieve the following API information through this website: https://my.telegram.org/apps
api_id = os.environ.get("telegram_api_id")
api_hash = os.environ.get("telegram_api_hash")
phone_number = os.environ.get("phone_number") # Make sure to include the country code


# # Create the client and connect. Commented out the following 1 line
# # use sequential_updates=True to respond to messages one at a time
client = TelegramClient(f"anon", api_id, api_hash, sequential_updates=True)
client.start(phone_number)


if __name__ == '__main__':
    print('Program initiated')
    client.send_message("me", "Initiating program")
    
    client.run_until_disconnected()



