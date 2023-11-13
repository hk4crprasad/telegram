from telethon import TelegramClient, events
from time import sleep
import itertools
import requests
import telethon
import json
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()
api_id = 16491177
api_hash = '7ec1aa5cf6f80a5260c8ac41334988cf'
excluded_channel_ids = [-1001525048796, -1001830204325, -1001458804740]
flood_counter = {}
max_flood_attempts = 5
client = TelegramClient('user', api_id, api_hash).start()
image_url = 'https://raw.githubusercontent.com/hk4crprasad/ph/master/HK4CRPRASAD_free-file.png'
response = requests.get(image_url)
with open('fetched_image.png', 'wb') as file:
    file.write(response.content)
message_intro = "🌟 **Hello, fabulous soul!** 🌈\n\nThank you for reaching out! 🚀\nI'm currently on a fabulous journey, but I'll get back to you soon.\n\n💫 **Join Now:** [JOIN NOW @JIREN_MODS](https://t.me/JIREN_MODS)\n\n⏳ **Fabulous Progress:** "
online = False
offline_user_ids = set()

@client.on(events.UserUpdate)
async def handle_update(event):
    global online
    user = await event.client.get_me()
    if user.status and getattr(user.status, 'online', False):
        online = True
        print("You are online!")
        if offline_user_ids:
            with open('/sdcard/ids.json', 'w') as ids_file:
                json.dump(list(offline_user_ids), ids_file)
    else:
        online = False

@client.on(events.NewMessage())
async def handler(event):
    global online
    global flood_counter
    global offline_user_ids
    sender = await event.get_input_sender()
    if sender and isinstance(sender, telethon.tl.types.User) and sender.user_id in excluded_channel_ids:
        return
    if event.message.sender_id == (await client.get_me()).id:
        return
    sleep(1)
    try:
        if not online:
            offline_user_ids.add(sender.user_id)
        if sender.user_id in flood_counter:
            flood_counter[sender.user_id] += 1
        else:
            flood_counter[sender.user_id] = 1
        if flood_counter[sender.user_id] > max_flood_attempts:
            print(f"Warning: User {sender.user_id} exceeded maximum allowed flood attempts. Blocking...")
            await client(telethon.tl.functions.contacts.BlockRequest(sender.user_id))
            return
        sent_message = await client.send_message(event.chat_id, message_intro + "⠋", file="fetched_image.png")
        previous_message_content = None
        for progress in itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]):
            if online:
                print("You are online! Script paused.")
                break
            sleep(0.1)
            updated_message = message_intro + f"Progress: {progress}\nFlood Attempts Left: {max_flood_attempts - flood_counter[sender.user_id]}"
            if updated_message != previous_message_content:
                await client.edit_message(event.chat_id, sent_message.id, updated_message)
                previous_message_content = updated_message
    except telethon.errors.rpcbaseerrors.ForbiddenError as e:
        if "CHAT_SEND_PHOTOS_FORBIDDEN" in str(e):
            print("ForbiddenError: Sending photos is not allowed in this chat.")
        elif "You can't write in this chat" in str(e):
            print("ForbiddenError: Writing messages is not allowed in this chat.")
        else:
            print(f"ForbiddenError: {e}")
    except telethon.errors.rpcerrorlist.MessageNotModifiedError:
        pass
client.run_until_disconnected()
keep_alive()