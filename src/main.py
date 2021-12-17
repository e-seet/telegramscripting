from telethon.sync import TelegramClient 

# Input the following information
# You can retrieve the following API information through this website: https://my.telegram.org/apps
api_id = "<YOUR_API_ID>"
api_hash = "<YOUR_API_HASH>"
phone_number = "<YOUR PHONE NUMBER>" # Make sure to include the country code


# # Create the client and connect. Commented out the following 1 line
client = TelegramClient(f"anon", api_id, api_hash, sequential_updates=True)
client.start(phone_number)

if __name__ == '__main__': # entry point of the application
    print('Program initiated')        
    client.run_until_disconnected()

