# main.py
from playwright.sync_api import sync_playwright

def run():
    try:
        with sync_playwright() as p:
            # Launch browser with user-agent to mimic a real browser
            browser = p.chromium.launch(headless=True)  # Set to False for debugging
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            # Navigate to Google with increased timeout
            print("Navigating to Google...")
            response = page.goto("https://www.google.com", timeout=60000)
            print(f"Page loaded with status: {response.status}")

            # Save a screenshot for debugging
            page.screenshot(path="google_page.png")
            print("Screenshot saved as google_page.png")

            # Check for consent page (common in some regions)
            consent_button = page.query_selector("button div:has-text('Accept')")
            if consent_button:
                print("Consent page detected, accepting...")
                consent_button.click()
                page.wait_for_timeout(2000)  # Wait for page to update

            # Wait for the search input
            print("Waiting for search input...")
            try:
                page.wait_for_selector("input[name='q']", timeout=15000)
                print("Search input found")
            except Exception as e:
                print(f"Search input not found: {str(e)}")
                print("Page content:", page.content()[:500])  # Print partial page content
                browser.close()
                return

            # Perform the search
            page.fill("input[name='q']", "prime minister in bd")
            page.keyboard.press("Enter")
            print("Search submitted")

            # Wait for search results
            page.wait_for_timeout(3000)
            print("Page title:", page.title())

            # Check for search results
            if page.query_selector("div#search"):
                print("Search results loaded successfully")
            else:
                print("Search results not found")

            browser.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run()