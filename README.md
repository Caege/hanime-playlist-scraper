



## Hanime Playlist Scraper

Extracts all playlists from a channel and saves every video URL into text files.

Each playlist → one `.txt` file
Each channel → its own folder

---

## Requirements

This tool uses a real browser (Playwright).
It **will NOT work** without installing the browser runtime.

### You must have

* Python 3.9+
* Internet connection
* ~300MB free space (for Playwright browser)

---

## Installation

```bash
git clone https://github.com/Caege/hanime-playlist-scraper.git
cd .\hanime-playlist-scraper\
```

Create environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

---

## Usage

```bash
python fetch_playlist_videos.py <channel_url>
```

Example:

```bash
python fetch_playlist_videos.py https://hanime.tv/channels/killua-3367
```

---

## Output

```
==================================================
Hanime Playlist Scraper
==================================================

[1/3] Fetching channel playlists...
✔ Found 10 playlists

Playlists:
  • Liked Videos (381 videos)
  • SUPERNOVA (300 videos)
  • QUALITY CONTENT (300 videos)
  • 🔥Best Of Uncensored 🔥 (133 videos)
  • MY ALL TIME FAVORITES (300 videos)
  • NTR (209 videos)
  • 🔥Fantasy and Elf🔥 (296 videos)
  • 🔥GREATEST OF ALL TIME 2.0🔥 (300 videos)
  • 🔥BunnyWalker\High Quality🔥 (300 videos)
  • 🔥Milf🔥 (204 videos)

--------------------------------------------------
[Playlist 1/10] Liked Videos

=== Liked Videos (381 videos, 16 pages) ===

📄 Page 1/16  [1-24]  → +24 videos  (15 pages left)
📄 Page 2/16  [25-48]  → +24 videos  (14 pages left)
📄 Page 3/16  [49-72]  → +24 videos  (13 pages left)

....
```

Each file contains direct video page URLs.

---

## Notes

* Script launches a headless Chromium browser
* First run is slow (browser install)
* Later runs are fast
* Do not close the terminal while running

---



## Why Playwright?

The website generates security tokens using JavaScript.
A normal HTTP scraper cannot access the API directly, so a browser runtime is required.


