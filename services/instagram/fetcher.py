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


import random
import requests
import os
from dotenv import load_dotenv
load_dotenv()
#utils
from ..utils.instahelps import shortcode_to_media_id , extract_shortcode

#fetched
class User:
    def __init__(self,userData):
        self.id = userData.get("id")
        self.fullname = userData.get("full_name")
        self.thumbail = userData.get("profile_pic_url_hd")
        self.username = userData.get("username")
        self.media_count = userData["edge_owner_to_timeline_media"]["count"]
        self.is_private = userData.get("is_private")
        self.is_verified = userData.get("is_verified")
        self.category_name = userData.get("category_name")
        self.is_professional_account = userData.get("is_professional_account")
        self.business_email = userData.get("business_email")
        self.business_phone_number = userData.get("business_phone_number")
        self.bio = f"{userData.get('biography')}"
        self.followers = f"{userData["edge_followed_by"]["count"]}"
        self.following = f"{userData["edge_follow"]["count"]}"
        self.is_business_account = userData.get("is_business_account")
        self.facebookID = userData.get("fbid")


#father 
class Ig:
    def __init__(self):
        # apis
        self.apis = {
    "single_highlight": "https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=highlight:{hg_id}",#
    "highlights": "https://i.instagram.com/api/v1/highlights/{user_id}/highlights_tray/",#
    "single_story": "https://i.instagram.com/api/v1/media/{media_id}/info/",#
    "stories": "https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={user_id}",#
    "profile": "https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",#
    "posts": "https://i.instagram.com/api/v1/feed/user/{user_id}/?count=40",
    "single_post": "https://i.instagram.com/api/v1/media/{media_id}/info/"
        }
        # headers
        USER_AGENTS = os.getenv("USER_AGENTS", "").split(",")
        IG_APP_IDS = os.getenv("IG_APP_IDS", "").split(",")
        COOKIE = os.getenv("SESSION_ID").split(",")
        #rotating user agent and ig-app-id
        user_agent = random.choice(USER_AGENTS)
        ig_app_id = random.choice(IG_APP_IDS)
        cookie = random.choice(COOKIE)
        self.headers = {
        "User-Agent": user_agent,
        "X-IG-App-ID": ig_app_id,  # هذا مثال لتطبيق Instagram الرسمي
        "Cookie": f"{cookie};"
        }
        # proxies
    
    ### functions  
    # Get Api  
    def getapi(self,key,**kwargs):
        return self.apis[key].format(**kwargs)
    # Get User Information
    def userInfo(self,username):
        res = requests.get(str(self.getapi("profile",username=username)),headers=self.headers,timeout=100)
        try:
            if res.status_code == 200:
                #data
                data = res.json()["data"]["user"]
                return User(data)
            else:
                return {"status":res.status_code,"message":"username not existing ."}
        except Exception as E:
            return {"status":"error","message": f"username not existing - {E}"}
    # Get Single Story
    def story(self,mediaID):
        res = requests.get(self.getapi("single_story",media_id=mediaID),headers=self.headers,timeout=100)
        try:
            if res.status_code == 200:
                data = res.json()
                item = data["items"][0]
                return {"Direct_url": item["video_versions"][0]["url"] if "video_versions" in item else item["image_versions2"]["candidates"][0]["url"] ,"type": "video" if "video_versions" in item else "photo"}
        except Exception as e:
            return {"status":res.status_code,"error":e}
    # Get User Stories
    def userStories(self,username):
        if self.userInfo(username).is_private:
            return {"status":"401","message":f"{username} account is private ."}
        userId = self.userInfo(username).id
        res = requests.get(self.getapi("stories",user_id=userId),headers=self.headers,timeout=100)
        try:
            if res.status_code == 200:
                data = res.json()
                story_ids = [story['id'] for story in data.get('reels', {}).get(str(userId), {}).get('items', [])]
                clean_ids = [i.split('_')[0] for i in story_ids]
                result = []
                for id in clean_ids:    
                    result.append(self.story(id))
                return result
            else:
                return {"status":"error","message":"Failed to fetch stories 💙."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    # Get Single Highlight
    def highlight(self,highlightID):
        res = requests.get(self.getapi("single_highlight",hg_id=highlightID),headers=self.headers)
        try:
            if res.status_code == 200:
                data = res.json()["reels"][f"highlight:{highlightID}"]["items"]
                highlights = []
                for i in data:
                    if "video_versions" in i:
                        highlights.append({"direct_url": i["video_versions"][0]["url"], "type": "video"})
                    else:
                        highlights.append({"direct_url": i["image_versions2"]["candidates"][0]["url"], "type": "photo"})
                return highlights
            else:
                return {"status":res.status_code,"message":"not responsed !"}
        except Exception as e:
            return {"status":"error","message":e}
    # Get Highlights
    def userhighlights(self,username):
        try:
            if self.userInfo(username).is_private:
                return {"status":"401","message":f"{username} account is private ."}
            userID = self.userInfo(username).id
            res = requests.get(self.getapi("highlights",user_id=userID),headers=self.headers,timeout=1000)
            if res.status_code == 200:
                data = res.json()["tray"]
                highlights = []
                direct_links = []
                for i in data:
                    highlights.append(i["id"].split(":")[1])
                for i in highlights:
                    direct_links.append(self.highlight(i))
                return direct_links
            else:
                return {"status":res.status_code,"message":"not responsed !"}
        except Exception as e:
            return {"status":"error","message":e}
    # Get post
    def post(self,url):
        try:
            shortcode = extract_shortcode(url)
            media_id = shortcode_to_media_id(shortcode)
            res = requests.get(self.getapi("single_post",media_id=media_id),headers=self.headers,timeout=1000)
            if res.status_code == 200:
                data = res.json()
                media_type = data["items"][0]["media_type"]
                if media_type == 1:
                    # صورة واحدة
                    image_url = data["items"][0]["image_versions2"]["candidates"][0]["url"]
                    caption = data["items"][0]["caption"]
                    return [{"direct_url": image_url,"caption": caption["text"] if caption else None  , "type":"image" , "slider":False}]
                elif media_type == 2:
                     # فيديو
                    video_url = data["items"][0]["video_versions"][0]["url"]
                    caption = data["items"][0]["caption"]
                    return [{"direct_url": video_url,"caption": caption["text"] if caption else None  , "type":"video" , "slider":False}]
                elif media_type == 8:
                    # carousel
                    carousel = {}
                    for i, item in enumerate(data["items"][0]["carousel_media"]):
                        if item["media_type"] == 1:
                           image_url = item["image_versions2"]["candidates"][0]["url"]
                           carousel[f"Image {i+1}"] = {"direct_url":image_url,"type":"image"}
                        elif item["media_type"] == 2:
                            video_url = item["video_versions"][0]["url"]
                            carousel[f"Video {i+1}"] = {"direct_url" : video_url, "type":"video"}
                    caption = data["items"][0]["caption"]
                    carousel["caption"] = caption["text"] if caption else None
                    carousel["slider"] = True
                    return [carousel]
            else:
                return {"status":404,"data":[]}
        except Exception as e:
            return {"status":404,"message":"Invalid Post ." ,"exception":e}

    # Get All Posts from user
    def userposts(self,username):
        try:
            if self.userInfo(username).is_private:
                return {"status":"401","message": f"{username} account is private ."}
            user_id = self.userInfo(username).id
            res = requests.get(self.apis["posts"].format(user_id=user_id),headers=self.headers)
            if res.status_code == 200:
                data = res.json()
                posts = []
                for item in data["items"]:
                    media_type = item["media_type"]
                    #picture
                    if media_type == 1:
                        image_url = item['image_versions2']['candidates'][0]['url']
                        posts.append({"type": "image", "direct_url": image_url})
                    elif media_type == 2:
                        video_url = item['video_versions'][0]['url']
                        posts.append({"type": "video", "direct_url": video_url})
                    elif media_type == 8:
                        for media in item["carousel_media"]:
                            if media["media_type"] == 1:
                                image_url = media['image_versions2']['candidates'][0]['url']
                                posts.append({"type": "image", "direct_url": image_url})
                            elif media['media_type'] == 2:
                                video_url = media['video_versions'][0]['url']
                                posts.append({"type": "video", "direct_url": video_url})
                return posts
            else:
                return {"status":res.status_code,"data":[]}
        except Exception as e:
            return {"status":"error","message":e}



