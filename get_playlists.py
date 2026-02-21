from playwright.sync_api import sync_playwright
import json
import re
import os
CHANNEL_URL = "https://hanime.tv/channels/killua-3367"


# ----------------------------
# utils
# ----------------------------

def safe_name(name: str) -> str:
    name = name.strip()

    # Windows forbidden characters
    name = re.sub(r'[<>:"/\\|?*]', "", name)

    # collapse whitespace
    name = re.sub(r"\s+", " ", name)

    return name


# ----------------------------
# scraping
# ----------------------------

def fetch_raw_playlists(channel_url):
    """Return (channel_name, raw_playlist_array_from_site)"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(channel_url, wait_until="domcontentloaded")

        # wait until Nuxt state exists
        page.wait_for_function(
            "() => window.__NUXT__ && window.__NUXT__.state && window.__NUXT__.state.data"
        )

        data = page.evaluate(
            """
            () => ({
                channel: window.__NUXT__.state.data.channel.user_channel.title,
                playlists: window.__NUXT__.state.data.channel.user_channel_playlists
            })
            """
        )

        browser.close()

    channel_name = safe_name(data["channel"])
    return channel_name, data["playlists"]


# ----------------------------
# processing
# ----------------------------

def simplify_playlists(channel_name, playlists):
    """Convert huge Nuxt objects → clean minimal json"""

    cleaned = [
        {
            "title": p["title"].strip(),
            "count": p["count"],
            "slug": p["slug"],
        }
        for p in playlists
    ]

    return {
        "channel": channel_name,
        "playlists": cleaned
    }


# ----------------------------
# file output
# ----------------------------

def save_playlists(data, path="playlists.json"):
    folder = data["channel"]

    # ensure channel directory exists
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, path)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filepath

output_playlist_path = ""

def generate_playlists_file(channel_url,path="playlists.json"):
    """Main callable function for other scripts"""
    global output_playlist_path
    channel, raw = fetch_raw_playlists(channel_url)
    clean = simplify_playlists(channel, raw)
    output_playlist_path = save_playlists(clean, path)
    
    return clean


# ----------------------------
# CLI usage
# ----------------------------

if __name__ == "__main__":
    data = generate_playlists_file()

    print(f"\nFound {len(data['playlists'])} playlists for channel '{data['channel']}':\n")

    for p in data["playlists"]:
        print(f'{p["title"]} ({p["count"]}) -> {p["slug"]}')

    print(f"\nSaved → {output_playlist_path}")