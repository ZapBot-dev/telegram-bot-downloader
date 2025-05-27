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


import logging
import os
from dotenv import load_dotenv
import shutil
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo , Update
from telegram.ext import ContextTypes
from services.gen.general import DS
from services.instagram.instagram import Instagram
from services.instagram.fetcher import Ig as Fet
from services.utils.instahelps import extract_username
from services.snapchat.snapchat import Snapchat
# Setup logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[92m"
# Initialize the downloader service
download = DS()

# Function to handle sending general downloads (audio/video)
async def send_general(url,update:Update):

    # Handle SoundCloud and TED audio download
    if "soundcloud" in url or "www.ted.com" in url:
        waited = await update.message.reply_text("Audio Downloading ...⏳")
        path = f"./downloads/{update.effective_chat.id}/audio"
        #info loggin
        logging.info(f"{GREEN}⬇️  Download SOUNDCLOUD | TED request detected . Starting the process! {RESET}")
        print(download.download_video(url,type_="audio",path_save=path))
        # Check For Download Done
        if not os.path.exists(path):
            await update.message.reply_text("❌Service Not Responsed")
            logging.warning(f"{RED}❌ Service  SOUNDCLOUD & TED (YT-DLP) Not Responsed{RESET}")
            await waited.delete()
            return
        audio_files = [f for f in os.listdir(path) if f.lower().endswith((".mp3"))]
        for file_name in audio_files:
            file_path = os.path.join(path, file_name)
            try:
                await update.message.reply_audio(audio=open(file_path, "rb"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=file_name)]]))
            except Exception as e:
                logging.warning(f"{RED}❌ handler soundcloud & ted catch error {RESET} - exception : {e}")
                await update.message.reply_text(f"❌Failed To Send Video {file_name}: {e}")
        await waited.delete()
        if os.path.exists(f"./downloads/{update.effective_chat.id}"):
            shutil.rmtree(f"./downloads/{update.effective_chat.id}")
            return
        return
    
    # Handle TikTok, Facebook, and Twitter video downloads
    if "tiktok" in url or "facebook" in url or "twitter" in url:
        waited = await update.message.reply_text("Video Downloading ...⏳")
        path = f"./downloads/{update.effective_chat.id}/video"
        #info loggin
        logging.info(f"{GREEN}⬇️  Download TIKTOK | FACEBOOK | TWITTER request detected . Starting the process! {RESET}")
        gen = print(download.download_video(url,type_="video",path_save=path))
        # Check For Download Done
        if not os.path.exists(path):
            await update.message.reply_text("❌Service Not Responsed")
            logging.warning(f"{RED}❌ Service  FACEBOOK & TWITTER & TIKTOK (YT-DLP) Not Responsed{RESET}")
            await waited.delete()
            return
        audio_files = [f for f in os.listdir(path) if f.lower().endswith((".mp4"))]
        for file_name in audio_files:
            file_path = os.path.join(path, file_name)
            try:
                await update.message.reply_video(video=open(file_path, "rb"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=file_name)]]))
            except Exception as e:
                logging.warning(f"{RED}❌ handler  FACEBOOK & TWITTER & TIKTOK (YT-DLP) Not Responsed{RESET} - exception : {e}")
                await update.message.reply_text(f"❌Failed To Send Video {file_name}: {e}")
        await waited.delete()
        if os.path.exists(f"./downloads/{update.effective_chat.id}"):
            shutil.rmtree(f"./downloads/{update.effective_chat.id}")
            return
        return

        # If it's a generic video site or unsupported, prompt user to choose format
    keyboard = [
        [
            InlineKeyboardButton("🎵 Audio", callback_data="download_audio"),
            InlineKeyboardButton("🎥 Video", callback_data="download_video"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose The Type :", reply_markup=reply_markup)

# CallBack
async def send_general_video_buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query 
    await query.answer() # Acknowledge the callback to avoid Telegram timeouts
    
    # Retrieve previously stored URL and username from context
    url = context.user_data.get("url")
    username = context.user_data.get("username")

    # If a username exists, we're dealing with Instagram features (stories, highlights, posts)
    if username:
        message_id  = context.user_data.get("profile_message_id")
        # Delete the profile preview message before sending new content
        await context.bot.delete_message(chat_id=update.effective_chat.id,message_id=message_id)
        
        # Handle Instagram stories download
        if query.data == "download_stories":
            waited = await query.message.reply_text(f"{username} Stories Downloading ...⏳") 
            #info loggin
            logging.info(f"{GREEN}⬇️  Download INSTAGRAM STORIES FROM {username} request detected . Starting the process! {RESET}")
            await stories_sender(username,update,context)
            await waited.delete()
            return
        
        # Handle Instagram highlights download
        if query.data == "download_highlights":
            waited = await query.message.reply_text(f"{username} Highlights Downloading ...⏳") 
            #info loggin
            logging.info(f"{GREEN}⬇️  Download INSTAGRAM HIGHLIGHTS FROM {username} request detected . Starting the process! {RESET}")
            await highlights_sender(username,update,context)
            await waited.delete()
            return
        
        # Handle Instagram posts download
        if query.data == "download_posts":
            waited = await query.message.reply_text(f"{username} Posts Downloading ...⏳") 
            #info loggin
            logging.info(f"{GREEN}⬇️  Download INSTAGRAM POSTS FROM {username} request detected . Starting the process! {RESET}")
            await posts_sender(username,update,context)
            await waited.delete()
            return

    # If no URL or username is saved, notify the user
    if not url:
        await query.message.reply_text(" No URl / Username Saved ❌") 
    chat_id = update.effective_chat.id

    # Handle audio download request
    if query.data == "download_audio":
        waited = await query.edit_message_text("Audio Downloading Please Wait... ⏳")
        path = f"./downloads/{chat_id}/audio"

        # Start download
        #info loggin
        logging.info(f"{GREEN}⬇️  Download AUDIO TYPE request detected . Starting the process! {RESET}")
        print(download.download_video(url, type_="audio", path_save=path))
        audio_files = [f for f in os.listdir(path) if f.lower().endswith((".mp3", ".wav", ".ogg"))]
        # Check For Download Done
        if not os.path.exists(path):
            await update.message.reply_text("❌Service Not Responsed")
            logging.warning(f"{RED}❌#path not exists# Service  YOUTUBE & DAILYMOTION... AUDIO (YT-DLP) Not Responsed{RESET}")
            await waited.delete()
            return
        # If no files were downloaded
        if not audio_files:
            await query.message.reply_text("Audio Files Not Found ❌")
            logging.warning(f"{RED}❌#if no files were downloaded# Handler YOUTUBE & DAILTMOTION... AUDIO ... (YT-DLP) Not Responsed{RESET}")
            await waited.delete()
            return

        # Send audio files one by one
        for file_name in audio_files:
            file_path = os.path.join(path, file_name)
            try:
                await query.message.reply_audio(audio=open(file_path, "rb"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=file_name)]]))
            except Exception as e:
                logging.warning(f"{RED}❌ #send audio files# - Handler YOUTUBE & DAILTMOTION ... (YT-DLP) Not Responsed{RESET} - Exception : {e}")
                await query.message.reply_text(f"Faild Send Audio ❌ {file_name}: {e}")

        # Clean up and remove "downloading" message
        await waited.delete()
        shutil.rmtree(f"./downloads/{chat_id}", ignore_errors=True)
        return

    # Handle video download request
    if query.data == "download_video":
        waited = await query.edit_message_text("Video Downloading ...⏳")
        path = f"./downloads/{chat_id}/video"
        #info loggin
        logging.info(f"{GREEN}⬇️  Download AUDIO TYPE request detected . Starting the process! {RESET}")
        # Start download
        print(download.download_video(url, type_="video", path_save=path))
        # Check For Download Done
        if not os.path.exists(path):
            await update.message.reply_text("❌ Service Not Responsed")
            logging.warning(f"{RED}❌#path not exists# Service  YOUTUBE & DAILYMOTION... VIDEO (YT-DLP) Not Responsed{RESET}")
            await waited.delete()
            return
        
        video_files = [f for f in os.listdir(path) if f.lower().endswith(".mp4")]
        
        # If no video files found
        if not video_files:
            await query.message.reply_text("Video Files Not Found ❌")
            logging.warning(f"{RED}❌#if no files were downloaded# Handler YOUTUBE & DAILTMOTION... VIDEO ... (YT-DLP) Not Responsed{RESET}")
            await waited.delete()
            return

        media_group = [] # Group of up to 10 videos to send in one message
        for index, file_name in enumerate(video_files, start=1):
            file_path = os.path.join(path, file_name)
            media_group.append(InputMediaVideo(media=open(file_path, "rb")))

            # Telegram allows up to 10 media per group
            if len(media_group) == 10 or index == len(video_files):
                    try:
                        await query.message.reply_media_group(media=media_group)
                    except Exception as e:
                        await query.message.reply_text(f"Failed Send Videos ❌")
                    finally:
                        media_group = []  # Reset group for next batch
        # Final cleanup
        await waited.delete()
        shutil.rmtree(f"./downloads/{chat_id}", ignore_errors=True)
    

# handle snapchat URLs
async def snapchat_handler(url,update:Update,context:ContextTypes.DEFAULT_TYPE):
    Snap = Snapchat()
    path = f"./downloads/{update.effective_chat.id}/"
    waited = await update.message.reply_text("Spotlight Downloading Please Wait ...⏳")
    #info loggin
    logging.info(f"{GREEN}⬇️  Download SNAPCHAT SPOTLIGHT request detected . Starting the process! {RESET}")
    # Handle URl
    if "https://www.snapchat.com/spotlight" in url:
        try:
            print(Snap.video(url,file_save=f"{path}/"))
            # Check For Download Done
            if not os.path.exists(f"{path}/video.mp4"):
                logging.warning(f"{RED}❌#no path exists# Service SNAPCHAT Not Responsed{RESET}")
                await update.message.reply_text("❌ Snapchat Service Not Responsed")
                await waited.delete()
                return   
            # send
            with open(f"{path}/video.mp4","rb") as video:
                await update.message.reply_video(
                    video=video,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=f"{path}/video.mp4")]])
                    )
            await waited.delete()
            if os.path.exists(path):
                shutil.rmtree(path)
            return

        except Exception as e:
            await waited.delete()
            await update.message.reply_text("❌ Service Not Responsed")
            logging.warning(f"{RED}❌ Handler SNAPCHAT Not Responsed{RESET} - exception : {e}")
            logging.warning({"status":"error","message":e})
            if os.path.exists(path):
                shutil.rmtree(path)


#handle instagram URLs
async def instagram_handler(url,update: Update,context:ContextTypes.DEFAULT_TYPE):
    Ig = Instagram()
    path = f"./downloads/{update.effective_chat.id}/"
    # Handle post, reel, or slider URLs
    if "/p/" in url or "/reel" in url:
        # Clean reels URL if needed
        if "instagram.com/reels/" in url:
            url = url.replace("reels/", "reel/")
        try:
            # Notify user that download is in progress
            waited = await update.message.reply_text("Post Downloading Please Wait ...⏳")
            #info loggin
            logging.info(f"{GREEN}⬇️  Download POST request detected . Starting the process! {RESET}")
            print(Ig.post(url=url,file_save=path))
        except Exception as e:
            print(f"🚫 Error: {e}")
            await update.message.reply_text("Downloaded Post Failed 🚫")
            return
        
        # If the path doesn’t exist (failed on first try), retry
        if not os.path.exists(path):
             logging.warning(f"{RED}❌#no path exists# Service INSTAGRAM REEL / P Not Responsed{RESET}")
             print(Ig.post(url=url,file_save=path))

        files = sorted(os.listdir(path)) # Get all downloaded files
        media_group = []

        # Send media in batches of 10 (Telegram media group limit)
        for i in range(0,len(files),10):
            media_group.clear()
            batch = files[i:i+10]
            for file in batch:
                file_path = os.path.join(path,file)
                if file.lower().endswith(('.jpg','.jpeg',".png")):
                    media_group.append(InputMediaPhoto(open(file_path,'rb')))
                elif file.lower().endswith(('.mp4','.mov',".webm")):
                    media_group.append(InputMediaVideo(open(file_path,'rb')))
            if media_group:
                sent_messages = await context.bot.send_media_group(chat_id=update.effective_chat.id,media=media_group)
                # Get and send post caption
                caption = Fet().post(url)[0]["caption"]
                await waited.delete()
                if caption:
                    await context.bot.send_message(chat_id=update.effective_chat.id,text=caption[:1024] ,reply_to_message_id=sent_messages[0].message_id)
        
        # Clean up
        if os.path.exists(path):
            shutil.rmtree(path)
        return
    
    # Handle Instagram highlights
    if "stories/highlights" in  url:
        try:
            waited = await update.message.reply_text("highlight Downloading Please Wait ...⏳")
            #info loggin
            logging.info(f"{GREEN}⬇️  Download HIGHLIGHT request detected . Starting the process! {RESET}")
            print(Ig.highlight(url=url,file_save=path))
            # Send video if exists, otherwise send image
            if not os.path.exists(f"{path}"):
                logging.warning(f"{RED}❌#no path exists# Service INSTAGRAM highlgihts Not Responsed{RESET}")
                await waited.delete()
                return
            if os.path.exists(f"{path}/video.mp4"):
                await update.message.reply_video(video=open(f"{path}video.mp4","rb"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=f"{path}/video.mp4")]]))
            else:
                await update.message.reply_photo(photo=open(f"{path}image.jpg","rb"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=f"{path}/image.jpg")]]))
        except Exception as e:
            logging.warning(f"{RED}❌ handler INSTAGRAM highlgihts Not Responsed{RESET} - exception : {e}")
            await update.message.reply_text("Downloaded Story Failed")
            
        if os.path.exists(path):
            shutil.rmtree(path)
        await waited.delete()
        return
    
    # Handle Instagram stories
    if "stories" in  url:
        try:
            waited = await update.message.reply_text("Story Downloading Please Wait ...⏳")
            #info loggin
            logging.info(f"{GREEN}⬇️  Download STORY request detected . Starting the process! {RESET}")
            print(Ig.story(url=url,file_save=path))
            if not os.path.exists(f"{path}"):
                logging.warning(f"{RED}❌#no path exists# Service INSTAGRAM stories Not Responsed{RESET}")
                await waited.delete()
                return
            if os.path.exists(f"{path}/video.mp4"):
                await update.message.reply_video(video=open(f"{path}video.mp4","rb"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=f"{path}/video.mp4")]]))
            else:
                await update.message.reply_photo(photo=open(f"{path}image.jpg","rb"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share", switch_inline_query=f"{path}/image.jpg")]]))
        except Exception as e:
            logging.warning(f"{RED}❌ handler INSTAGRAM stories Not Responsed{RESET} - exception : {e}")
            await update.message.reply_text("Downloaded Story Failed 🚫")
            
        if os.path.exists(path):
            shutil.rmtree(path)
        await waited.delete()
        return
    

    # Handle Instagram profile lookup by username
    else:
        try:
            username = extract_username(url)
            waited = await update.message.reply_text("Searching Please Wait ...⏳")
            data = Ig.Profile(username)
            thumbnail = data["thumbail"]
            res_thumbnail = requests.get(thumbnail)
            os.makedirs(path, exist_ok=True)
            thumPATH = f"{path}image.jpg"
            
            with open(thumPATH,"wb") as thum:
                thum.write(res_thumbnail.content)
            if os.path.exists(thumPATH):
                # Create keyboard buttons
                keyboard = None
                reply_markup = None
                if data["is_private"]:
                    keyboard[[InlineKeyboardButton("Private Account 🔒",url=f'https://www.instagram.com/{data["username"]}')]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                else:
                    keyboard = [
                        [InlineKeyboardButton("Visit  🔗",url=f'https://www.instagram.com/{data["username"]}')],
                        [InlineKeyboardButton("📖 Stories", callback_data="download_stories")],
                        [InlineKeyboardButton("✨ Latest Highlights", callback_data="download_highlights")],
                        [InlineKeyboardButton("🆕 Latest Posts", callback_data="download_posts")],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                
                # Save username and profile message id in user data
                context.user_data["username"] = username
                #info loggin
                logging.info(f"{GREEN}⬇️ @{username} PROFILE-INFORMATION-INSTAGRAM POST request detected . Starting the process! {RESET}")
                profile =  await update.message.reply_photo(
                    photo=open(thumPATH,"rb"),
                    caption=f"""
🪪 {data["fullname"]} - 🆔 {data["id"]}
followers 😍 : {data["followers"]}
following 👣 : {data["following"]}
Posts 🏞 : {data["media_count"]}
{"" if data["bio"] == "" else data["bio"]}
------------------------------------------------
                    """,
                    reply_markup= reply_markup
                )
                context.user_data["profile_message_id"] = profile.message_id
            else:
                await update.message.reply_text(f"Thumbnail Not Found 🚫")
        except Exception as e:
            print(f"🚫 Error: {e}")
            await update.message.reply_text(f"Username Not Found 🚫")
        
        if os.path.exists(path):
            shutil.rmtree(path)
        await waited.delete()
        return
    


# Function to send Instagram Stories from a username

async def stories_sender(username,update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    path = f"./downloads/{chat_id}/"

    try:
        # Download all available stories for the username
        Instagram().stories(username,file_save=path)
        files = sorted(os.listdir(path)) # List all downloaded files
        media = []

        # Process and group media for Telegram
        for i, f in enumerate(files):
            p = os.path.join(path, f)
            if f.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                media.append(InputMediaPhoto(open(p, 'rb')))
            elif f.endswith(('.mp4', '.mov', '.mkv', '.webm')):
                media.append(InputMediaVideo(open(p, 'rb')))

            # Send media in groups of 10 or if it's the last batch
            if len(media) == 10 or i == len(files) - 1:
                await context.bot.send_media_group(chat_id, media)
                media = []

        # Clean up downloaded files
        if os.path.exists(path):
            shutil.rmtree(path)

    except Exception as e:
        print(f"🚫 Error: {e}")
        await context.bot.send_message(chat_id,f"Stories Not Found 🚫")


# Function to send latest Instagram Highlights
async def highlights_sender(username,update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    path = f"./downloads/{chat_id}/"

    try:
        # Download the latest highlights for the username
        Instagram().latestHighighlts(username,file_save=path)
        files = sorted(os.listdir(path)) # List all downloaded files
        media = []

        # Process and group media for Telegram
        for i, f in enumerate(files):
            p = os.path.join(path, f)
            if f.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                media.append(InputMediaPhoto(open(p, 'rb')))
            elif f.endswith(('.mp4', '.mov', '.mkv', '.webm')):
                media.append(InputMediaVideo(open(p, 'rb')))

             # Send media in groups of 10 or if it's the last batch
            if len(media) == 10 or i == len(files) - 1:
                await context.bot.send_media_group(chat_id, media)
                media = []

        

    except Exception as e:
        print(f"🚫 Error: {e}")
        await context.bot.send_message(chat_id,f"Highlights Not Found 🚫")

    finally:
        # Clean up downloaded files
        if os.path.exists(path):
            shutil.rmtree(path)
            
# Function to send latest Instagram Posts
async def posts_sender(username,update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    path = f"./downloads/{chat_id}/"

    try:
        # Download the latest posts for the username
        Instagram().latestPosts(username,file_save=path)
        files = sorted(os.listdir(path)) # List all downloaded files
        media = []

        # Process and group media for Telegram
        for i, f in enumerate(files):
            p = os.path.join(path, f)
            if f.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                media.append(InputMediaPhoto(open(p, 'rb')))
            elif f.endswith(('.mp4', '.mov', '.mkv', '.webm')):
                media.append(InputMediaVideo(open(p, 'rb')))

            # Send media in groups of 10 or if it's the last batch
            if len(media) == 10 or i == len(files) - 1:
                await context.bot.send_media_group(chat_id, media)
                media = []

        # Clean up downloaded files
        if os.path.exists(path):
            shutil.rmtree(path)

    except Exception as e:
        print(f"🚫 Error: {e}")
        await context.bot.send_message(chat_id,"Posts Not Found 🚫")



