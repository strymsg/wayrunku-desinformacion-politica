"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import logging
from playsound import playsound

async def handle_captcha(page):
    try:
        # Check for the presence of the CAPTCHA dialog
        captcha_dialog = page.locator('div[role="dialog"]')
        is_captcha_present = await captcha_dialog.count() > 0 and await captcha_dialog.is_visible()
        count = 0
        if is_captcha_present:
            logging.info("CAPTCHA detected. Please solve it manually.")
            playsound('../../common/resources/fx-cartoon-94472.mp3', block=False)
            # Wait for the CAPTCHA to be solved
            await page.wait_for_selector('div[role="dialog"]', state='detached', timeout=470000)  # 7 minutes timeout
            logging.info("CAPTCHA solved. Resuming script...")
            await asyncio.sleep(0.5)  # Short delay after CAPTCHA is solved
    except Exception as e:
        logging.error(f"Error while handling CAPTCHA: {str(e)}")    
