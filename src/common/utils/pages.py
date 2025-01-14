"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

from src.common.utils.time import random_sleep


async def scroll_page(page):
    """Scroll pages to the bottom using Playwright javascript

    Params:
    page (playwrigth page)
    """
    await page.evaluate("""
        window.scrollBy(0, window.innerHeight);
    """)
    await random_sleep(0.8, 2.9)

