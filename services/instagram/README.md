# Instagram Content Scraper API (Unofficial)

This Python project allows you to **fetch data from Instagram** such as:
- User profile info
- Stories
- Highlights
- Posts (single images, carousels, videos)

## Features

- ✅ Get user ID from username
- ✅ Fetch and download posts by shortcode
- ✅ Fetch stories and highlights for a user
- ✅ Automatically detects post type (video/image/carousel)
- ✅ Returns metadata (likes, caption, views, comments count...)

## Usage

Make sure to install dependencies first (if any).

```bash
pip install -r requirements.txt
```

Then use it in your Python script:

```python
from instagram import InstagramScraper

ig = InstagramScraper()
user_id = ig.get_user_id("instagram")
posts = ig.get_user_posts(user_id)
```

## Notes

- This tool uses public endpoints and does not require login or token.
- It may break if Instagram updates its frontend or API structure.


# DOWNLOADER

This module provides a set of methods to interact with Instagram and download user-related content such as profiles, stories, highlights, and posts.

## Features

- 🔍 Fetch detailed profile info
- 📥 Download individual stories, highlights, and posts
- 📚 Retrieve and download all available stories, highlights, and posts from a public profile

## Usage

Import the class and call the methods accordingly:

```python
from instagram import Instagram

ig = Instagram()

# Get profile information
profile = ig.Profile("username")

# Download a post
ig.post("https://www.instagram.com/p/XXXXXXXXXXX/")

# Download all posts from a user
ig.latestPosts("username")

# Download all stories from a user
ig.stories("username")

# Download all highlights from a user
ig.latestHighighlts("username")

# Download a single story
ig.story("https://www.instagram.com/stories/highlights/XXXXXXXX/")

# Download a single highlight
ig.highlight("https://www.instagram.com/stories/highlights/XXXXXXXX/")
```

## Dependencies

- `requests`
- `os`
- Custom Modules:
  - `utils.validator`
  - `instagram.fetcher`

## Notes

- Ensure the username is valid and public for story and post retrieval.
- Files will be saved in the `./downloads` directory by default.

## License

This project is for educational purposes only. Not affiliated with or endorsed by Instagram.


> © 2025 Amine Bouzaid 