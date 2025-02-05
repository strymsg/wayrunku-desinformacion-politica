"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

from playsound import playsound
from src.tiktok.scraper.locators import locators
from src.common.utils.selectors import get_locator, get_selector_value
from src.common.utils.custom_logger import CustomLogger


LOGGER = CustomLogger('tiktok utils 🔨:')

async def handle_captcha(page):
    try:
        # Check for the presence of the CAPTCHA dialog
        captcha_dialog = page.locator('div[role="dialog"]')
        is_captcha_present = await captcha_dialog.count() > 0 and await captcha_dialog.is_visible()
        # check for the presence of login container
        is_login_container_present = await check_if_login_container(page)

        if is_captcha_present and not is_login_container_present:
            LOGGER.info("CAPTCHA detected. Please solve it manually.")
            playsound('/home/rodrigo.garcia/Misc/Misc/internetBo/desinformación_política/p_obtencion_datos/wayrunku-desinformacion-politica/src/common/resources/MarioBrosPiano.mp3', block=False)
            # Wait for the CAPTCHA to be solved
            await page.wait_for_selector('div[role="dialog"]', state='detached', timeout=472000)  # 7 minutes timeout
            LOGGER.info("CAPTCHA solved. Resuming script...")
            await asyncio.sleep(0.5)  # Short delay after CAPTCHA is solved
    except Exception as e:
        LOGGER.error(f"Error while handling CAPTCHA: {str(e)}")


async def check_if_login_container(page):
    try:
        login_container = page.locator(get_locator(locators['common']['loginContainer']))
        is_login_container_present = await login_container.count() > 0 and await login_container.is_visible()
        if is_login_container_present:
            LOGGER.info('LOGIN CONTAINER detected, trying to close.')
            await login_container.click()
            return True
    except Exception as e:
        LOGGER.debug(f'Error trying to close login container: {str(e)}')
        return False
    return False
