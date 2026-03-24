import asyncio
from playwright.async_api import async_playwright

async def search_youtube(query: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Searching YouTube for: {query}")
        await page.goto(f"https://www.youtube.com/results?search_query={query}")

        # Wait for content to load
        await page.wait_for_selector('ytd-video-renderer')

        # Extract first few results
        videos = await page.query_selector_all('ytd-video-renderer')
        results = []
        for video in videos[:3]:
            title_elem = await video.query_selector('#video-title')
            title = await title_elem.inner_text() if title_elem else "No Title"
            
            link = await title_elem.get_attribute('href') if title_elem else "No Link"
            
            meta_elem = await video.query_selector('#metadata-line')
            meta_text = await meta_elem.inner_text() if meta_elem else "No Meta"

            results.append({
                "title": title.strip(),
                "link": f"https://www.youtube.com{link}",
                "meta": meta_text.replace('\n', ' • ').strip()
            })

        for i, res in enumerate(results):
            print(f"[{i+1}] {res['title']} ({res['meta']})")

        await asyncio.sleep(5) # Allow visualization
        await browser.close()
        return results

if __name__ == "__main__":
    asyncio.run(search_youtube("dancing cat"))
