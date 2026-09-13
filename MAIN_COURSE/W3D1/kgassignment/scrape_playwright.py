import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.tn.gov.in"
LIST_URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

def scrape_tn_schemes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("Opening scheme directory...")
        page.goto(LIST_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_load_state("networkidle")

        # 1. Collect scheme links from the listing
        links = page.locator("a").all()
        scheme_urls = []
        for link in links:
            href = link.get_attribute("href") or ""
            title = link.inner_text().strip()
            # Match detail links on the portal
            if "scheme_data_view.php" in href or "scheme" in href.lower():
                full_url = href if href.startswith("http") else f"{BASE_URL}/{href.lstrip('/')}"
                if full_url not in [item["url"] for item in scheme_urls] and len(title) > 3:
                    scheme_urls.append({"title": title, "url": full_url})

        print(f"Discovered {len(scheme_urls)} scheme links. Scraping details...")

        # If direct detail links weren't found, extract general table rows from the page
        schemes_data = []
        if not scheme_urls:
            print("No individual scheme links found. Extracting page body text directly...")
            body_text = page.locator("body").inner_text()
            schemes_data.append({
                "title": "Agriculture and Allied Schemes Directory",
                "details": body_text[:4000]
            })
            browser.close()
            return schemes_data

        # 2. Visit each scheme page and extract structured criteria
        # Limited to first 10 for clean ingestion and API speed
        for item in scheme_urls[:10]:
            try:
                print(f"Fetching: {item['title']}...")
                page.goto(item["url"], wait_until="domcontentloaded", timeout=30000)
                
                # Extract text or structured definition lists/tables
                content_text = page.locator("body").inner_text()
                
                # Keep meaningful content
                lines = [line.strip() for line in content_text.splitlines() if len(line.strip()) > 30]
                summary = " \n".join(lines[:15])

                schemes_data.append({
                    "title": item["title"],
                    "url": item["url"],
                    "details": summary
                })
                time.sleep(1)
            except Exception as err:
                print(f"Skipped {item['title']}: {err}")

        browser.close()
        return schemes_data

if __name__ == "__main__":
    schemes = scrape_tn_schemes()
    print(f"\nSuccessfully collected {len(schemes)} schemes.")

    with open("schemes.json", "w", encoding="utf-8") as f:
        json.dump(schemes, f, indent=2, ensure_ascii=False)
    
    print("Saved results to schemes.json")