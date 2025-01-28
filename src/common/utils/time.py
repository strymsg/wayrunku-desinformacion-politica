"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import asyncio, random
from datetime import datetime as dt

async def random_sleep(min_seconds, max_seconds):
    await asyncio.sleep(random.uniform(min_seconds, max_seconds))


def today_yyyymmdd() -> str:
    """Returns today date in format YYYY-MM-DD"""
    return dt.strftime(dt.now(), '%Y-%m-%d')
