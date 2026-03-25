from playwright.async_api import async_playwright, Browser, BrowserContext
import asyncio
from typing import List, Dict, Any

class WebAgent:
    """Advanced Web Browser Agent with optimization to reduce latency."""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None

    async def _ensure_browser(self):
        """Initializes browser instance if not already running (Singleton pattern)."""
        if self._browser is None:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=self.headless)
            self._context = await self._browser.new_context()
            print("[*] WebAgent: Browser instance initialized (Warm Start ready).")

    async def search_youtube(self, query: str) -> str:
        """Searches YouTube and returns result. Uses existing browser context to reduce latency."""
        print(f"[*] WebAgent: Searching YouTube for '{query}'...")
        
        try:
            await self._ensure_browser()
            page = await self._context.new_page()
            
            # Go to YouTube Search
            url = f"https://www.youtube.com/results?search_query={query}"
            await page.goto(url)
            
            # Wait for video items to load
            await page.wait_for_selector('ytd-video-renderer', timeout=10000)
            
            # Extract top 3 videos
            videos = await page.evaluate('''() => {
                const items = Array.from(document.querySelectorAll('ytd-video-renderer')).slice(0, 3);
                return items.map(item => ({
                    title: item.querySelector('#video-title')?.innerText || 'No Title',
                    link: item.querySelector('#video-title')?.href || '',
                    channel: item.querySelector('#channel-info')?.innerText || '',
                    view_count: item.querySelector('#metadata-line span:first-child')?.innerText || '',
                    duration: item.querySelector('#overlays #text')?.innerText || 'N/A'
                }));
            }''')
            
            await page.close() # Close page but keep context/browser alive
            
            if not videos:
                return "유튜브에서 검색 결과를 찾지 못했습니다."
            
            response = f"유튜브에서 '{query}'에 대한 검색 결과입니다:\n\n"
            for i, v in enumerate(videos, 1):
                response += f"{i}. [{v['title']}] ({v['duration']})\n   - 채널: {v['channel']} / {v['view_count']}\n   - 링크: {v['link']}\n\n"
            
            response += "가장 마음에 드는 영상을 실행해 드릴까요?"
            return response
        except Exception as e:
            print(f"[!] WebAgent Error: {e}")
            return f"유튜브 검색 중 오류가 발생했습니다: {str(e)}"

    async def close(self):
        """Cleanup browser resources."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

# Instance for manager
web_agent = WebAgent(headless=False)
