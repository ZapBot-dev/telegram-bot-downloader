# Media Downloader with `yt_dlp`

This project provides a simple Python class `DS` for downloading videos or audio from YouTube and other supported platforms using the `yt_dlp` library. It supports both single media links and playlists, and outputs the files to a specified directory.

## Features

- Download full videos or extract audio only (MP3 format).
- Supports playlists or single URLs.
- Custom output directory.
- Clean error handling with validation logic.
- Uses `yt_dlp` for media processing.

## Requirements

- Python 3.6+
- `yt_dlp` library
- `ffmpeg` installed and added to PATH (for audio extraction)
- A `validator` module that contains a `DS_VALIDATOR()` function to check URL validity

## Installation

1. Clone this repository or copy the source code.
2. Install required Python packages:
   ```bash
   pip install yt-dlp
   ```

3. Make sure `ffmpeg` is installed and available on your system.

## Project Structure

```
your_project/
├── downloader.py       # Contains the DS class
├── utils/
│   └── validator.py    # Contains the validator class and DS_VALIDATOR function
```

## Usage

```python
from downloader import DS

ds = DS()

# Example: Download video
video_files = ds.download_video(
    url="https://www.youtube.com/watch?v=example",
    type_="video",
    filepath=[],
    path_save="downloads"
)

# Example: Download audio
audio_files = ds.download_video(
    url="https://www.youtube.com/watch?v=example",
    type_="audio",
    filepath=[],
    path_save="downloads"
)
```

### Parameters

- `url`: The link to the video or playlist.
- `type_`: `"video"` for full video, `"audio"` for audio only (mp3).
- `filepath`: A list to store output paths (pass an empty list).
- `path_save`: Directory to save the downloaded files (optional).

### Return Value

A list of downloaded file paths.

### Output Naming

- Single file: `video_1.mp4` or `audio_1.mp3`
- Playlist: `video_1.mp4`, `video_2.mp4`, ..., `audio_1.mp3`, `audio_2.mp3`, etc.

## Error Handling

- If an unsupported URL is passed, returns:
  ```json
  {"status": "error", "message": "You passed unsupported url ."}
  ```

- Prints clear messages in case of `yt_dlp` or other exceptions.

## License

This project is for educational and personal use. Make sure to follow the terms of service of any media platform you are using.


> © 2025 Amine Bouzaid