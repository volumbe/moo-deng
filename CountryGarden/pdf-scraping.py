import asyncio
from playwright.async_api import async_playwright, Page


COUNTRY_GARDEN_DOMAIN="https://www.bgy.com.cn"
COUNTRY_GARDEN_PDF_URL="https://www.bgy.com.cn/en/mobile/investor/notice"

async def get_pdf_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url, timeout=120000)
        await page.wait_for_timeout(2000)

        pdf_links = []
        for year in range(2017, 2025):  # Iterate from 2017 to 2024
            await select_year(year, page)
            await page.wait_for_timeout(2000)  # Wait for content to load after year selection
            for month in range(11):
                await select_month(month, page)
                await page.wait_for_timeout(2000)  # Wait for content to load after month selection
                month_pdf_links = await get_pdf_links_from_page(page)
                pdf_links.extend(month_pdf_links)

        return pdf_links

async def select_year(year: int, page: Page):
    month_input = page.locator("#monthSelete")
    await month_input.click()
    await page.wait_for_timeout(500)
    
    year_input = page.locator("div[class='laydate-set-ym']")
    await year_input.click()
    await page.wait_for_timeout(1000)

    await page.locator(f"li[lay-ym='{year}']").click()
    await page.wait_for_timeout(500)
    
    await page.locator("li[lay-ym='0']").click()

    print(f"Selected year: {year}")

async def select_month(month: int, page: Page):
    month_input = page.locator("#monthSelete")
    await month_input.click()

    await page.locator(f"li[lay-ym='{month}']").click()
    print(f"Selected month: {month}")


async def get_pdf_links_from_page(page: Page):
    pdf_links = await page.evaluate('''
        () => {
            const listDiv = document.querySelector('div.List');
            if (!listDiv) return [];
            
            const links = listDiv.querySelectorAll('a');
            return Array.from(links).map(link => link.href);
        }
    ''')
    return pdf_links

async def main():
    pdf_links = await get_pdf_content(COUNTRY_GARDEN_PDF_URL)
    for link in pdf_links:
        print(f"Processing PDF link: {link}")
        # Add your logic here to process each PDF link

if __name__ == "__main__":
    asyncio.run(main())