from flask import Flask
from threading import Thread
import time
import requests

app = Flask('')
link = " https://telegram-bot-downloader-f0x2.onrender.com" # ex : https://telegram-bot-downloader-f0x2.onrender.com
@app.route('/')
def home():
    return "I’m alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
    def self_ping():
        while True:
            try:
                print("[Pinger] Sending request to self...")
                requests.get(f"{linlk}:8080/")
            except Exception as e:
                print(f"[Pinger] Failed to ping self: {e}")
            time.sleep(200)  

    ping_thread = Thread(target=self_ping)
    ping_thread.start()
