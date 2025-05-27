
import re



class validator:
    def __init__(self):
        self.regex_patterns = [
    r'^https?://youtu\.be/[a-zA-Z0-9_-]{11}(\?.*)?$',
    r'^https?://(www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+(&.*)?$',
    r'^https?://(www\.)?youtube\.com/shorts/[a-zA-Z0-9_-]+(\?.*)?$',
    r'^https?://(www\.)?vimeo\.com/[0-9]+(\?.*)?$',
    r'^https?://(www\.)?dailymotion\.com/video/[a-zA-Z0-9]+(\?.*)?$',
    r'^https?://(www\.|web\.)facebook\.com/share/.+',
    r'^https?://(www|web)\.facebook\.com/[^/]+/videos/\d+(/)?(\?.*)?$',
    r'^https?://(www\.)?twitter\.com/.+?/status/\d+(\?.*)?$',
    r'^https?://(www\.)?x\.com/.+?/status/\d+(\?.*)?$',
    r'^https?://(www\.)?tiktok\.com/@[^/]+/video/\d+(\?.*)?$',
    r'^https?://(www\.)?soundcloud\.com/[^/]+/[^/]+(\?.*)?$',
    r'^https?://(www\.)?twitch\.tv/videos/\d+(\?.*)?$',
    r'^https?://(www\.)?bilibili\.com/video/[a-zA-Z0-9]+(\?.*)?$',
    r'^https?://(www\.)?nicovideo\.jp/watch/[a-zA-Z0-9]+(\?.*)?$',
    r'^https?://(www\.)?ted\.com/talks/[^/]+(\?.*)?$',
    r'^https?://(www\.)?reddit\.com/r/[^/]+/comments/\w+/[^/]+(\?.*)?$'
]

        self.regex_instagram = [
            r"^https:\/\/www\.instagram\.com\/"
        ]

    def DS_VALIDATOR(self,url:str):
        for pattern in self.regex_patterns:
            if re.match(pattern,url):
                return True
        return False
    
    def instagram(self,url:str):
        for pattern in self.regex_instagram:
            if re.match(pattern,url):
                return True
        return False



