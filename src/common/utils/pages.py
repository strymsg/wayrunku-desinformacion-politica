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

