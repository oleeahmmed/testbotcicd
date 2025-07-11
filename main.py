# main.py
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.fill("input[name='q']", "prime minister in bd")
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)
        print(page.title())
        browser.close()

if __name__ == "__main__":
    run()
