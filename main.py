import sys
import json
import time
import requests
import asyncio
import websocket
from flask import Flask
from threading import Thread
from multiprocessing import Process

app = Flask(__name__)

# Votre token va entre les crochets.
usertoken = "token"

# GUILD_ID est l'identifiant du serveur et CHANNEL_ID est l'identifiant du canal vocal.
GUILD_ID = 322116541216566
CHANNEL_ID = 11656175176521

# Ne pas changer, sauf si vous voulez vous mettre en mode hors ligne, ou désactiver le mode muet et sourdine
# (il est déjà configuré pour être en mode muet et sourdine et en ligne).
SELF_MUTE = True
SELF_DEAF = True
status = "online"


# Ne pas modifier ici, mais en bas pour les messages de la ligne 120 à 125. by Furkan 
headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Votre token pourrait être invalide. Veuillez le vérifier.")
    sys.exit()

userinfo = validate.json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows"
            },
            "presence": {
                "status": status,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    
    vc = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": SELF_MUTE,
            "self_deaf": SELF_DEAF
        }
    }
    
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    app.run(host='0.0.0.0', port=8080)

def run_joiner():
    print(f"Connecté en tant que {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)
        time.sleep(30)

def run_sender():
    send_messages_with_intervals(channel_id, message_intervals)

def send_message(channel_id, message_content):
    message_data = {"content": message_content}
    response = requests.post(f"https://discordapp.com/api/v9/channels/{channel_id}/messages", headers=headers, json=message_data)
    
    if response.status_code == 200:
        print("Message bien envoyé")
    else:
        print(f"Message non envoyé. Status code : {response.status_code}")
        print(response.text)

def send_messages_with_intervals(channel_id, message_intervals):
    while True:
        for interval in message_intervals:
            message = interval["message"]
            delay_seconds = interval["delay_seconds"]
            send_message(channel_id, message)
            time.sleep(delay_seconds)

if __name__ == "__main__":
    userinfo = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers).json()
    username = userinfo["username"]
    discriminator = userinfo["discriminator"]
    userid = userinfo["id"]

# Configurer ici les messages. channel_id est l'identifiant du canal textuel. Il suffit de le remplacer.
# ATTENTION : veuillez bien respecter l'exemple, sinon cela ne fonctionnera pas.
# Remplacer le delai du message en seconde par le delai de votre message en seconde
    channel_id = 23456455651195
    message_intervals = [
        {"message": "votre message ici", "delay_seconds": le delai du message en seconde},
        # Voici un exemple
        {"message": "exemple", "delay_seconds": 40},
    ]
    
    flask_process = Process(target=keep_alive)
    flask_process.start()

    joiner_thread = Thread(target=run_joiner)
    sender_thread = Thread(target=run_sender)

    joiner_thread.start()
    sender_thread.start()

    joiner_thread.join()
    sender_thread.join()

    flask_process.join()

