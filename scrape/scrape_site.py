import os
import json
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_with_openai(raw_text):
    prompt = f"""
You are given raw text scraped from a webpage. Clean and structure this text into a JSON object with sections if possible. 
Return only valid JSON. Example format:
{{
  "sections": [
    {{
      "title": "Section Title",
      "content": "Text content of the section."
    }},
    ...
  ]
}}

Raw text:
\"\"\"
{raw_text}
\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1000,
    )
    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"⚠️ Failed to parse OpenAI response: {e}")
        return {}

def scrape_site(start_url, output_file="knowledge.json", max_pages=20):
    visited = set()
    data = {"sections": []}

    def is_same_domain(base, url):
        return urlparse(url).netloc == urlparse(base).netloc or urlparse(url).netloc == ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        to_visit = [start_url]

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue

            try:
                page.goto(url, timeout=15000)
                print(f"Scraping: {url}")

                raw_text = page.evaluate(
                    """
                    () => {
                        function getVisibleText(element) {
                            if (!element) return "";
                            if (element.nodeType === Node.TEXT_NODE) {
                                if (element.parentElement && window.getComputedStyle(element.parentElement).visibility === "hidden") return "";
                                return element.textContent.trim();
                            }
                            if (element.nodeType === Node.ELEMENT_NODE) {
                                const style = window.getComputedStyle(element);
                                if (style.visibility === "hidden" || style.display === "none") return "";
                                let text = "";
                                for (const child of element.childNodes) {
                                    text += getVisibleText(child) + " ";
                                }
                                return text.trim();
                            }
                            return "";
                        }
                        return getVisibleText(document.body);
                    }
                    """
                )

                cleaned = clean_with_openai(raw_text)
                if "sections" in cleaned and isinstance(cleaned["sections"], list):
                    data["sections"].extend(cleaned["sections"])

                visited.add(url)

                links = page.locator("a").evaluate_all("elements => elements.map(e => e.href)")
                for link in links:
                    if is_same_domain(start_url, link) and link not in visited and link not in to_visit:
                        to_visit.append(link)

            except Exception as e:
                print(f"⚠️ Failed to scrape {url}: {e}")

        browser.close()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(data['sections'])} sections into {output_file}")

if __name__ == "__main__":
    scrape_site("https://magnoliacake.com.au", max_pages=30)  # Replace with your site