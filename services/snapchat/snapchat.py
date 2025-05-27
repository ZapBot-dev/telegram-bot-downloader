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


import requests 
from bs4 import BeautifulSoup
import os



class Snapchat():
    def __init__(self):
        # headers
        USER_AGENTS = os.getenv("SNAP_USER_AGENTS")
        self.headers = {
            "User-Agent": USER_AGENTS,
            "Referer": "https://www.snapchat.com/"
        }
    def video(self,url,file_save="./downloads"):
        try:
            if not "https://www.snapchat.com/spotlight/" in url:
                return {"status":"error","message":"link invalid ."}
            res = requests.get(url,headers=self.headers ,stream=True)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                video_tag = soup.find('video')
                if video_tag and video_tag.has_attr('src'):
                    os.makedirs(file_save, exist_ok=True)
                    full_path = os.path.join(file_save, "video.mp4")
                    with open(full_path,"wb") as f:
                        f.write(requests.get(video_tag['src']).content)
                    
                    return {"status":res.status_code, "path": full_path}
                else:
                    source_tag = soup.find('source')
                    if source_tag and source_tag.has_attr('src'):
                        os.makedirs(file_save, exist_ok=True)
                        full_path = os.path.join(file_save, "video.mp4")
                        with open(full_path,"wb") as f:
                            f.write(requests.get(source_tag['src']).content)
                        return {"status":res.status_code, "message":"video downloaded "}
                    else:
                        return {"status":"404","message":"Video URL Not Found ❌"}
            else:
                return {"status":res.status_code,"direct_url":""}
        except Exception as e:
            return {"status":"error","message":"download failed .","exception":str(e)}
    
    
