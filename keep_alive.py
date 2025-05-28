from flask import Flask
from threading import Thread
import time
import requests

app = Flask('')

@app.route('/')
def home():
    return "I’m alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # شغل السيرفر في ثريد منفصل
    t = Thread(target=run)
    t.start()
    
    # استهداف السيرفر نفسه كل فترة عشان يفضل نشط
    def self_ping():
        while True:
            try:
                print("[Pinger] Sending request to self...")
                requests.get("https://telegram-bot-downloader-f0x2.onrender.com:8080/")
            except Exception as e:
                print(f"[Pinger] Failed to ping self: {e}")
            time.sleep(600)  # كل 10 دقائق

    ping_thread = Thread(target=self_ping)
    ping_thread.start()
