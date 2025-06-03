"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

from src.common.utils.time import random_sleep
from src.common.utils.custom_logger import CustomLogger


LOGGER = CustomLogger("utils")


async def scroll_page(page):
    """Scroll pages to the bottom using Playwright javascript

    Params:
    page (playwrigth page)
    """
    LOGGER.debug(" scrolling page")
    await page.evaluate("""
        window.scrollBy(0, window.innerHeight);
    """)
    await random_sleep(0.8, 2.9)


async def scroll_down_pixels(page, pixels=400):
    """Scrolls down the given amount of pixels
    """
    LOGGER.debug(f" scrolling page {pixels} pixels...")
    await page.evaluate(f"""
        window.scrollBy(0, {pixels});
    """)
    await random_sleep(1, 2.4)


async def scroll_up_pixels(page, pixels=400):
    """Scrolls up the given amount of pixels
    TODO: Test better
    """
    LOGGER.debug(f" scrolling up page {pixels} pixels...")
    await page.evaluate(f"""
        window.scrollBy(0, -{pixels});
    """)
    await random_sleep(1, 2.4)
