# -----------------------------------------------------------------------------
# MIT License
# 
# Copyright (c) 2025 Amine Bouzaid
# Creator GitHub: https://github.com/ZapBot-dev 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
import time
import asyncio
import logging
import os
import threading
from dotenv import load_dotenv
import flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler,filters,CallbackQueryHandler
)
from donation import donation
from services.utils import validator
from handlers import send_general , send_general_video_buttons_handler , instagram_handler , snapchat_handler
from channel import is_user_member
from limit import is_allowed_to_use
# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv("BOT_TOKEN")
POLLING_MOOD = os.getenv("POLLING_MOOD", "TRUE") == "TRUE"
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
DONATION_SYSTEM = os.getenv("DONATION_SYSTEM")
IS_MAINTENANCE = os.getenv("IS_MAINTENANCE")
# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_user_member(user_id):
        await update.message.reply_text(f"❌ follow the channel to use it :\n👉 @{CHANNEL_USERNAME}")
        return
    await update.message.reply_text(
        "👋 Welcome to your ultimate content downloader bot 🚀\n"
        "I'm here to help you easily and quickly download media from your favorite platforms 📥\n\n"
        "🎯 Just send a link, and I’ll handle the rest 💡\n"
        "💬 Supported platforms: TikTok, Instagram, YouTube...\n\n"
        "🔒 Everything you send stays 100% private and secure\n"
        f"— Powered by {CHANNEL_USERNAME} 🤖"
    )

# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🛠️ **How to Use the Bot**\n\n"
        f"📌 Just send a link or a username — I'll handle the rest!\n\n"
        f"**✅ Supported Platforms & Features:**\n"
        f"• 📸 Instagram – Posts, Stories, Highlights, Profile Info\n"
        f"• 🎵 TikTok – Videos, Profiles\n"
        f"• 🐦 Twitter – Video downloads\n"
        f"• 📘 Facebook – Video downloads\n"
        f"• 📺 YouTube – Video & Audio downloads\n"
        f"• 🔊 SoundCloud – Audio downloads\n"
        f"• 🎤 TED – Talk downloads\n"
        f"• 📼 Dailymotion – Video & Audio\n"
        f"• 🎬 Vimeo – Video & Audio\n\n"
        f"**📥 Examples:**\n"
        f"`https://www.instagram.com/username/`\n"
        f"`tiktok.com/@user/video/123...`\n"
        f"`instagram username` (just the username)\n\n"
        f"🔒 Your data stays private and is never stored.\n"
        f"📢 Stay updated or get support: {CHANNEL_USERNAME}\n\n"
        f"🚀 Developed by: {CHANNEL_USERNAME}"
)
    return


# Handle regular text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #maintenance 
    if IS_MAINTENANCE.upper() == "TRUE":
        await update.message.reply_text("""
        🚧 Server Maintenance In Progress 🛠️
We're currently performing scheduled maintenance to improve your experience.

⏳ Please bear with us — the bot will be back shortly!
Thank you for your patience ❤️
""")
        return
    user_id = update.effective_user.id

    # Check if user is a member of the required channel
    if not is_user_member(user_id):
        await update.message.reply_text(f"❌ follow the channel to use it :\n👉 @{CHANNEL_USERNAME}")
        return
    
    chat_id = update.effective_chat.id
    url = update.message.text
    message = update.message or update.channel_post

    if not message or not message.text:
        return  
    
    url = message.text
    # limit
    allowed , message = is_allowed_to_use(context.user_data)
    if not allowed:
        await update.message.reply_text(message)
        return

    # Process URLs
    if "https://" in url:
        if validator.validator().DS_VALIDATOR(url):
            context.user_data["url"] = url
            await send_general(url, update)
            logger.info(f"Processed supported URL from user {user_id}.")
            #DONATION_SYSTEM
            if DONATION_SYSTEM == "activate":
                # ⏱️ Track how many times the user used the bot
                count = context.user_data.get("donation_counter", 0)
                context.user_data["donation_counter"] = count + 1
                # 🎯 Every 7 uses, show donation message
                if context.user_data["donation_counter"] % 7 == 0:
                    await donation(update)
            return
        elif validator.validator().instagram(url):
            await instagram_handler(url,update,context)
            logger.info(f"Processed Instagram URL from user {user_id}.")
            #DONATION_SYSTEM
            if DONATION_SYSTEM == "activate":
                # ⏱️ Track how many times the user used the bot
                count = context.user_data.get("donation_counter", 0)
                context.user_data["donation_counter"] = count + 1
                # 🎯 Every 7 uses, show donation message
                if context.user_data["donation_counter"] % 7 == 0:
                    await donation(update)
            return
        elif "https://www.snapchat.com/spotlight" in url:
            await snapchat_handler(url,update,context)
            #DONATION_SYSTEM
            if DONATION_SYSTEM == "activate":
                # ⏱️ Track how many times the user used the bot
                count = context.user_data.get("donation_counter", 0)
                context.user_data["donation_counter"] = count + 1
                # 🎯 Every 7 uses, show donation message
                if context.user_data["donation_counter"] % 7 == 0:
                    await donation(update)
            return
    elif not "https://" in url:
        new_url = f"https://www.instagram.com/{url}" 
        await instagram_handler(new_url,update,context)
        logger.info(f"Processed assumed Instagram username for user {user_id}.")
        #DONATION_SYSTEM
        if DONATION_SYSTEM == "activate":
                # ⏱️ Track how many times the user used the bot
                count = context.user_data.get("donation_counter", 0)
                context.user_data["donation_counter"] = count + 1
                # 🎯 Every 7 uses, show donation message
                if context.user_data["donation_counter"] % 7 == 0:
                    await donation(update)
        return
    # Invalid or unsupported URL
    await update.message.reply_text("Please Provide a Supported URl !")
    logger.warning(f"User {user_id} sent an unsupported or invalid URL.")


#run bot as flask
def run_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

# Flask setup
app = flask.Flask(__name__)

@app.route('/')
def home():
    return 'Telegram bot is running via Flask on Render! ✅'

def visit_site():
    url = "https://example.com"
    while True:
        try:
            response = requests.get(url)
            print(f"[{time.ctime()}] Visited {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"[{time.ctime()}] Error: {e}")
        time.sleep(120)

# main
def main():
    # POLLING_MOOD
    app = ApplicationBuilder().token(TOKEN).read_timeout(200).write_timeout(300).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(send_general_video_buttons_handler))
    app.run_polling()
    print("✅ Bot is running...")

#calling server
asyncio.create_task(visit_site())
# FLASK MOOD
if not POLLING_MOOD:
    print("✅ Starting bot with webhook mode...")  
    if __name__ == '__main__':
        threading.Thread(target=run_bot_thread).start()
        app.run(host='0.0.0.0', port=5000)
else:
    if __name__ == '__main__':
        main()
