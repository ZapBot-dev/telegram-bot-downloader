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
import yt_dlp
from ..utils.validator import validator

    
class DS:
    def __init__(self):
        self.video_opts = {
            'format': 'best',
            'quiet': True,
            'noplaylist': False,
        }
        self.audio_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    def download_video(self, url: str, type_: str, filepath: list = [], path_save: str = None) -> list:
        checkingLink = validator().DS_VALIDATOR(url)
        if not checkingLink:
            return {"status": "error", "message": "You passed unsupported url."}

        options = self.video_opts.copy() if type_ == "video" else self.audio_opts.copy()

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                infos = ydl.extract_info(url, download=False)

                if 'entries' in infos:
                    # Playlist
                    for idx, entry in enumerate(infos['entries'], start=1):
                        if type_ == "audio":
                            # استخدم عنوان الموسيقى كاسم
                            title = entry.get('title', f'audio_{idx}')
                            safe_title = ''.join(c for c in title if c.isalnum() or c in ' _-').strip()
                            out_path = os.path.join(path_save, f"{safe_title}.mp3") if path_save else f"{safe_title}.mp3"
                            options['outtmpl'] = out_path
                        else:
                        # فيديو = اسم ثابت
                            custom_name = f"video_{idx}.mp4"
                            out_path = os.path.join(path_save, custom_name) if path_save else custom_name
                            options['outtmpl'] = out_path

                        with yt_dlp.YoutubeDL(options) as inner_ydl:
                            inner_ydl.download([entry['webpage_url']])
                        filepath.append(out_path)

                else:
                    # Single file
                    if type_ == "audio":
                        title = infos.get('title', 'audio_1')
                        safe_title = ''.join(c for c in title if c.isalnum() or c in ' _-').strip()
                        out_path = os.path.join(path_save, f"{safe_title}.mp3") if path_save else f"{safe_title}.mp3"
                        options['outtmpl'] = out_path
                    else:
                        custom_name = "video_1.mp4"
                        out_path = os.path.join(path_save, custom_name) if path_save else custom_name
                        options['outtmpl'] = out_path

                    with yt_dlp.YoutubeDL(options) as single_ydl:
                        single_ydl.download([url])
                    filepath.append(out_path)

        except yt_dlp.utils.DownloadError as e:
            print({"ERROR": f"Download failed: {str(e)}", "message": "Invalid Link."})
        except Exception as e:
            print({"ERROR": f"Unexpected error: {str(e)}", "message": "Something went wrong."})
        finally:
            print("Download Operation Completed.")

        return filepath


