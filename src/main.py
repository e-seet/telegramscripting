import time
from telethon.sync import TelegramClient, events
import requests
import json
import urllib
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

#giphy
giphy_api_key =os.environ.get("giphy_api")
 
print(os.getcwd())
def checkEnvironment():
    print(api_hash)
    print(phone)
    print(api_id)

checkEnvironment()


#file =  "C:\\Users\\eddie\\Desktop\\telegram coding\\"

def getgif():
    url = "https://api.giphy.com/v1/gifs/random?api_key=" +giphy_api_key+ "&tag=&rating=R"
    #r = requests.get(url = url)
    #print(r.url)
    #print(r.content)

    #response = urllib.request.urlopen(url).read()
    response = urllib.request.urlopen(url).read()
    jsonResponse = json.loads(response.decode('utf-8'))


    endurl = jsonResponse["data"]["images"]["original"]["mp4"] 
    key = jsonResponse["data"]["id"]


    r = requests.get("https://i.giphy.com/media/" + key  + "/giphy.mp4", allow_redirects=True)
    open("../gifdump/file.mp4","wb").write(r.content)


    thefile = "../gifdump/file.mp4"
    return thefile

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

client.send_message(me, "Hello myself")


if __name__ == '__main__':
    # The trigger that replies
    @client.on(events.NewMessage())
    async def handle_message(event):
        print("Got your message")
        print(event.from_id)
        client.send_file('me', getgif())
        # print(event)
        # await event.respond(f'Saved your photo babe')

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        if event.is_private:  # only auto-reply to private chats
            _from = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
            print(f"From: {_from}")
            if not _from.bot:  # skip auto-reply to bots
                print(time.asctime(), '-', event.message)  # optionally log time and message
                time.sleep(1)  # pause for 1 second to rate-limit automatic replies

                #if this particular person messages me.
                if  event.message.peer_id.user_id ==555332310:
                    #send file to this particular person. (can be another person as well. So take note of the telegram username in the case"Johnnyboiii")
                    await client.send_file('me', getgif())
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



