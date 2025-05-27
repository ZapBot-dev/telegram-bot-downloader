from urllib.parse import urlparse

def shortcode_to_media_id(shortcode):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    media_id = 0
    for char in shortcode:
        media_id = media_id * 64 + alphabet.index(char)
    return str(media_id)

def extract_shortcode(url):
    parts = url.split("/")
    for i, part in enumerate(parts):
        if part in ["p", "reel", "tv"]:
            if i + 1 < len(parts):
                return parts[i + 1]
    return None



def extract_username(url):
    path = urlparse(url).path
    username = path.strip('/').split('/')[0]
    return username