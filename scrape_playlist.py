import requests
import json
from get_headers import get_signed_headers

BASE = "https://cached.freeanimehentai.net/api/v8/playlist_hentai_videos"
PLAYLIST_ID = "kcqyjfmyyzhajhff4r9s"

headers = get_signed_headers()

params = {
    "playlist_id": PLAYLIST_ID,
    "__order": "sequence,DESC",
    "__offset": 72,
    "__count": 24,
    "personalized": 1
}

r = requests.get(BASE, headers=headers, params=params)

print("STATUS:", r.status_code)

# convert to python object
data = r.json()

# pretty print to console
print("\nPRETTY JSON:\n")
print(json.dumps(data, indent=2)[:5000])

# save full json to file
with open("playlist_page_0.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nSaved → playlist_page_0.json")