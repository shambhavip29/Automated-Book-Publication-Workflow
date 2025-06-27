# scrape_chapter.py

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os

def scrape_content(url, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Set a realistic browser User-Agent to avoid getting blocked
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
        })

        try:
            print("🌐 Navigating to URL...")
            page.goto(url, timeout=15000)

            # Wait for body to load
            page.wait_for_selector("body", timeout=10000)

            # Check for rate limiting (429 errors)
            page_text = page.inner_text("body")
            if "429" in page_text or "Too Many Requests" in page_text:
                print("❌ Blocked by Wikimedia (429 Too Many Requests). Try again later.")
                return ""

            # Save screenshot
            screenshot_path = os.path.join(output_dir, "screenshot.png")
            page.screenshot(path=screenshot_path, full_page=True)

            # Save scraped text
            text_path = os.path.join(output_dir, "raw_text.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(page_text)

            print(f"✅ Scraping complete.\n📄 Text saved at: {text_path}\n🖼️ Screenshot saved at: {screenshot_path}")
            return page_text

        except PlaywrightTimeoutError:
            print("❌ Page took too long to load. Please check your internet or the site status.")
            return ""

        except Exception as e:
            print(f"❌ Unexpected error during scraping: {e}")
            return ""

        finally:
            browser.close()

# Test independently
if __name__ == "__main__":
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    scrape_content(url)
