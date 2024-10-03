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
        
        for year in range(2024, 2005, -1):  # Iterate from 2024 to 2005
            await page.wait_for_timeout(2000)  # Wait for content to load after year selection
            for month in range(12):
                await select_month(month, page)
                await page.wait_for_timeout(2000)  # Wait for content to load after month selection
                month_pdf_links = await get_pdf_links_from_page(page)
                pdf_links.extend(month_pdf_links)
            await go_prev_year(page)
        await browser.close()
        return pdf_links

async def open_date_range(page: Page):
    month_input = page.locator("#monthSelete")
    await month_input.click()
    await page.wait_for_timeout(500)

async def go_prev_year(page: Page):
    await open_date_range(page)
    await page.locator("[class='layui-icon laydate-icon laydate-prev-y']").click()
    await page.wait_for_timeout(500)

    await page.locator("li[lay-ym='0']").click()
    await page.wait_for_timeout(500)


async def select_month(month: int, page: Page):
    await open_date_range(page)

    await page.locator(f"li[lay-ym='{month}']").click()

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
    with open("pdf_links.txt", "w") as file:
        for link in pdf_links:
            file.write(f"{link}\n")

if __name__ == "__main__":
    asyncio.run(main())