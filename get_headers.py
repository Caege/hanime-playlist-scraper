from playwright.sync_api import sync_playwright

INIT_PAGE = "https://hanime.tv/channels/killua-3367"

def get_signed_headers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(INIT_PAGE, wait_until="domcontentloaded")

        # wait until signer is ready
        page.wait_for_function("() => window.ssignature && window.stime")

        signature = page.evaluate("window.ssignature")
        stime = page.evaluate("window.stime")

        browser.close()

        return {
            "x-signature": signature,
            "x-time": str(stime),
            "x-signature-version": "web2",
            "referer": "https://hanime.tv/",
            "origin": "https://hanime.tv",
            "user-agent": "Mozilla/5.0",
            "accept": "application/json",
            "content-type": "application/json",
        }


if __name__ == "__main__":
    h = get_signed_headers()
    print("\n=== SIGNED HEADERS ===\n")
    for k, v in h.items():
        print(f"{k}: {v}")