import asyncio
import threading
import time
from playwright.async_api import async_playwright
from app import create_app

def run_server():
    app = create_app()
    app.run(port=5005, use_reloader=False, debug=False)

# Start Flask in background
t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(3)

async def main():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Login
            print("Logging in...")
            await page.goto("http://127.0.0.1:5005/auth/login")
            await page.fill("input[name='username']", "superboss")
            await page.fill("input[name='password']", "superboss")
            await page.click("button[type='submit']")
            await page.wait_for_load_state("networkidle")
            
            # Navigate to upload page
            print("Navigating to upload...")
            await page.goto("http://127.0.0.1:5005/catalog/upload")
            
            # Check if we got there
            print("Setting file...")
            await page.set_input_files("input[type='file']", r"c:\Users\HP\Desktop\Stock\daryza_productos_formato_requerido.csv")
            
            # Click upload
            print("Submitting...")
            await page.click("button[type='submit']")
            
            # Wait a few seconds for response and animation
            print("Waiting for response...")
            await page.wait_for_timeout(3000)
            
            # Save screenshot
            await page.screenshot(path=r"c:\Users\HP\Desktop\Stock\error_repro.png")
            print("Screenshot saved to error_repro.png")
            
            # Extract any visible alert or toast text
            html = await page.content()
            if "Error al procesar" in html:
                print("FOUND ERROR TEXT IN HTML")
            
            await browser.close()
    except Exception as e:
        print("Playwright script failed:", e)

asyncio.run(main())
