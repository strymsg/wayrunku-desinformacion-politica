"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import asyncio, random


async def random_sleep(min_seconds, max_seconds):
    await asyncio.sleep(random.uniform(min_seconds, max_seconds))


