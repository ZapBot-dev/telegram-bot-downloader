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


import os
from ..utils.validator import validator
import requests
from ..instagram import fetcher as fetcher
from dotenv import load_dotenv
load_dotenv()
# limit downloading
stories_limit = (os.getenv("stories_limit")).upper()
posts_limit = os.getenv("posts_limit").upper()
highlights_limit = os.getenv("highlights_limit").upper()

class Instagram():
    def __init__(self):
        pass
    # Porfile information
    def Profile(self,username):
        try:
            userinformation = fetcher.Ig().userInfo(username)
            return {
                "id":userinformation.id,
                "fullname" : userinformation.fullname,
                "username":userinformation.username,
                "bio": userinformation.bio,
                "followers": userinformation.followers,
                "following": userinformation.following,
                "facebookID": userinformation.facebookID,
                "media_count" : userinformation.media_count,
                "is_private": userinformation.is_private,
                "is_verified": userinformation.is_verified,
                "category_name": userinformation.category_name,
                "is_professional_account": userinformation.is_professional_account,
                "business_email": userinformation.business_email,
                "business_phone_number": userinformation.business_phone_number,
                "is_business_account": userinformation.is_business_account,
                "thumbail": userinformation.thumbail,
            }
        except Exception as e:
            return {"status":"error","message":f"username not existing || {e}"}
    # Story
    def story(self,url,file_save="./downloads"):
        if not validator().instagram(url):
                return {"status":"error","message":"link invalid ."}
        try:
            mediaID =  url.rstrip("/").split("/")[-1]
            data = fetcher.Ig().story(mediaID)
            os.makedirs(file_save, exist_ok=True)
            full_path = None
            if str(data["type"]) == "video":
                full_path = os.path.join(file_save, "video.mp4")
            else:
                full_path = os.path.join(file_save, "image.jpg")
            with open(full_path,"wb") as f:
                res = requests.get(data["Direct_url"],timeout=1000)
                f.write(res.content)
            return {"status":"ok","message":f'{data["type"]} downloaded .'}


        except Exception as e:
            return {"status":"err","message":f"story invalid || {e}"}
    # Highlight 
    def highlight(self,url,file_save="./downlaods"):
        if not validator().instagram(url):
                return {"status":"error","message":"link invalid ."}
        try:
            mediaID =  url.rstrip("/").split("/")[-1]
            data = fetcher.Ig().highlight(mediaID)
            os.makedirs(file_save, exist_ok=True)
            full_path = None
            if data[0]["type"] == "video":
                full_path = os.path.join(file_save, "video.mp4")
            else:
                full_path = os.path.join(file_save, "image.jpg")
            with open(full_path,"wb") as f:
                res = requests.get(data[0]["direct_url"],timeout=1000)
                f.write(res.content)
            return {"status":"ok","message":f"{data[0]["type"]} downloaded ."}
        except Exception as e:
            return {"status":"error","message":"highlight invalid","exception":e}
    # post
    def post(self,url,file_save="./downloads"):
        if not validator().instagram(url):
            return {"status":"error","message":"link invalid ."}
        try:
            data = fetcher.Ig().post(url)
            os.makedirs(file_save, exist_ok=True)
            full_path = None
            if not data[0]["slider"]:
                if data[0]["type"] == "video":
                    full_path = os.path.join(file_save, "video.mp4")    
                else:
                    full_path = os.path.join(file_save, "image.jpg")
                with open(full_path,"wb") as f:
                    res = requests.get(data[0]["direct_url"],timeout=1000)
                    f.write(res.content)
                return {"status":"ok","message":f"{data[0]["type"]} downloaded ."}
            else:
                for i in range(1,(len(data[0])-1)):
                    key = f"Image {i}"
                    key_2 = f"Video {i}"
                    #return len(data[0])
                    if key in data[0]:
                        if data[0][key]["type"] == "image":
                            full_path = os.path.join(file_save, f"image{i}.jpg")  
                        with open(full_path,"wb") as f:
                            res = requests.get(data[0][key]["direct_url"],timeout=1000)
                            f.write(res.content)
                    else:
                        if data[0][key_2]["type"] == "video":
                            full_path = os.path.join(file_save, f"video{i}.mp4")
                        with open(full_path,"wb") as f:
                            res = requests.get(data[0][key_2]["direct_url"],timeout=1000)
                            f.write(res.content)
                return {"status":"ok","message": "Slider downloaded ."}

        except Exception as e:
             return {"status":"error","message":"post invalid .","exception":e}
    # stories
    def stories(self,username,file_save = "./downloads"):
        try:
            if self.Profile(username)["is_private"]:
                return {"status":"error","message":f"{username} is private account ."}
            data = fetcher.Ig().userStories(username)
            if len(data) == 0:
                return {"status":"success","message":f"{username} have no stories ."}
            os.makedirs(file_save, exist_ok=True)
            full_path = None
            for i in range(0,len(data)):
                if data[i]["type"] == "video":  
                    full_path = os.path.join(file_save, f"video{i}.mp4")    
                else:
                    full_path = os.path.join(file_save, f"image{i}.jpg")
                with open(full_path,"wb") as f:
                        res = requests.get(data[i]["Direct_url"],timeout=1000)
                        f.write(res.content)
                #limit downloading
                if i+1 == int(stories_limit):
                    break
                
            return {"status":"ok","message": "Stories downloaded ."}
        except Exception as e:
            return {"status":"error","message":f"{username} user invalid ." , "exception" : e}
    # highighlts
    def latestHighighlts(self,username,file_save = "./downloads"):
        try:
            if self.Profile(username)["is_private"]:
                return {"status":"error","message":f"{username} is private account ."}
            
            data = fetcher.Ig().userhighlights(username)
            
            if len(data) == 0:
                return {"status":"success","message":f"{username} have no highlights ."}
            os.makedirs(file_save, exist_ok=True)
            full_path = None
            file_idx = 0
            stop = False
            for idx in range(0,len(data)):
                for i in range(0,len(data[idx])):
                    #print(f"highlights number : {idx} :",data[idx])
                    if data[idx][i]["type"] == "video":
                        full_path = os.path.join(file_save, f"video{file_idx}.mp4") 
                    else:
                        full_path = os.path.join(file_save, f"image{file_idx}.jpg")
                    with open(full_path,"wb") as f:
                        res = requests.get(data[idx][i]["direct_url"],timeout=1000)
                        f.write(res.content)
                    file_idx += 1
                    #limit downloading
                    if file_idx == int(highlights_limit):
                        stop = True
                        break
                if stop:
                    break
            return {"status":"ok","message": "Highlights downloaded ."}
        except Exception as e:
            return {"status":"error","message":f"{username} user invalid ." , "exception" : e}
    # posts
    def latestPosts(self,username,file_save = "./downloads"):
        try:
            if self.Profile(username)["is_private"]:
                return {"status":"error","message":f"{username} is private account ."}
            data = fetcher.Ig().userposts(username)
            if len(data) == 0:
                return {"status":"success","message":f"{username} have no posts ."}
            os.makedirs(file_save, exist_ok=True)
            full_path = None
            for i in range(len(data)):
                if data[i]["type"] == "video":
                    full_path = os.path.join(file_save, f"video{i}.mp4") 
                else:
                    full_path = os.path.join(file_save, f"image{i}.jpg")
                with open(full_path,"wb") as f:
                        res = requests.get(data[i]["direct_url"],timeout=1000)
                        f.write(res.content)
                #limit downloading
                if i+1 == int(posts_limit):
                    break
            return {"status":"ok","message": "Posts downloaded ."}
        except Exception as e:
            return {"status":"error","message":f"{username} user invalid ." , "exception" : e}



