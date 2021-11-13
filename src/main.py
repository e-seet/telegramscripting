import time
from telethon import TelegramClient, events
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
message= "This user is asleep. Please do not distrub. ETR: ??"

# Create the client and connect
# use sequential_updates=True to respond to messages one at a time
with TelegramClient("anon", api_id, api_hash, sequential_updates=True) as client:


    to = "me"
    # The trigger that replies
    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):

        if event.is_private:  # only auto-reply to private chats
            from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon

            if not from_.bot:  # skip auto-reply to bots
                print(time.asctime(), '-', event.message)  # optionally log time and message
                time.sleep(1)  # pause for 1 second to rate-limit automatic replies
    
                #if this particular person messages me.
                if  event.message.peer_id.user_id ==555332310:
                    #send file to this particular person. (can be another person as well. So take note of the telegram username in the case"Johnnyboiii")
                    await client.send_file('Johnnyboiii',   getgif())
                if "detonate" in event.message.raw_text:
                    await client.send_message(to, "Detonating explosives. Countdown starting")
                    for i in range(5, 0, -1):
                        await client.send_message(to, str(i) + "...")
                        time.sleep(1)
                    await client.send_message(to, "That was a joke.")
                #if anyone elses.
                else:                
                    #spamm the poor guy anyways. :P
                    await client.send_file('Goopher', getgif())
                    #replies back to the original event with the message declared earlier.
                    response = generate_random_response()
                    await event.respond(response)

    print(time.asctime(), '-', 'Auto-replying...')

    async def main():
        response = generate_random_response()
        await client.send_message(to, response)
        
    # client.loop.run_until_complete(main())
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')



