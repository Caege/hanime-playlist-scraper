import math
import json
import requests
import os
from get_headers import get_signed_headers
from get_playlists import generate_playlists_file, safe_name

BASE = "https://cached.freeanimehentai.net/api/v8/playlist_hentai_videos"
PAGE_SIZE = 24
CHANNEL_URL = "https://hanime.tv/channels/killua-3367"


def fetch_playlist(slug, title):
    headers = get_signed_headers()

    offset = 0
    all_videos = []
    total_pages = None

    while True:
        params = {
            "playlist_id": slug,
            "__order": "sequence,DESC",
            "__offset": offset,
            "__count": PAGE_SIZE,
        }

        r = requests.get(BASE, headers=headers, params=params)

        if r.status_code == 401:
            print("🔄 Signature expired → refreshing")
            headers = get_signed_headers()
            continue

        payload = r.json()
        videos = payload["fapi"]["data"]
        meta = payload["fapi"]["meta"]

        # compute pages once
        if total_pages is None:
            total_pages = math.ceil(meta["total"] / PAGE_SIZE)
            print(f"\n=== {title} ({meta['total']} videos, {total_pages} pages) ===\n")

        page_num = offset // PAGE_SIZE + 1
        remaining = total_pages - page_num

        start_vid = offset + 1
        end_vid = min(offset + len(videos), meta["total"])

        print(
            f"📄 Page {page_num}/{total_pages}  "
            f"[{start_vid}-{end_vid}]  "
            f"→ +{len(videos)} videos  "
            f"({remaining} pages left)"
        )

        all_videos.extend(videos)
        offset += PAGE_SIZE

        if offset >= meta["total"]:
            print(f"✅ Completed {title}\n")
            break

    return all_videos


def main(channel_url):
    print("=" * 50)
    print("Hanime Playlist Scraper")
    print("=" * 50)
    print("\n[1/3] Fetching channel playlists...")

    # create channel folder
    data = generate_playlists_file(channel_url)
    print(f"✔ Found {len(data['playlists'])} playlists\n")
    print("Playlists:")
    for p in data["playlists"]:
        print(f"  • {p['title']} ({p['count']} videos)")
        
    os.makedirs(data["channel"], exist_ok=True)
    
    
    for idx, pl in enumerate(data["playlists"], start=1):
        print("\n" + "-" * 50)
        print(f"[Playlist {idx}/{len(data['playlists'])}] {pl['title']}")
        slug = pl["slug"]
        title = pl["title"]

        

        videos = fetch_playlist(slug, title)

        # OPTIONAL: convert to clean URLs
        urls = [f"https://hanime.tv/videos/hentai/{v['slug']}" for v in videos]

        filepath = os.path.join(data["channel"], f"{safe_name(title)}.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(urls))

        print(f"Saved {len(urls)} videos → {filepath}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fetch_playlist_videos.py <channel_url>")
        exit(1)

    url = sys.argv[1]
    main(url)

    