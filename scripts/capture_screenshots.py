"""Capture actual rendered previews. Requires: pip install playwright; playwright install chromium."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox'])
        semaphore = asyncio.Semaphore(4)
        async def capture(path):
            async with semaphore:
                page = await browser.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
                try:
                    await page.goto(path.as_uri(), wait_until='load', timeout=30000)
                    await page.wait_for_timeout(3500)
                    await page.screenshot(path=str(ROOT / 'thumbs' / (path.stem+'.jpg')), type='jpeg', quality=82, timeout=30000)
                    print(path.name, flush=True)
                finally:
                    await page.close()
        await asyncio.gather(*(capture(path) for path in sorted(ROOT.glob('[0-9][0-9][0-9]-*.html'))))
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
