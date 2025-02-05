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
    

def age_in_days(_datetime) -> int:
    """Given a datetime returns its age in days.
    Thus the days from that date to today"""
    return (dt.now() - _datetime).days


def datetime_from_yyyymmdd(datestr: str):
    """Returns the datetime object from the string in format yyyy-mm-dd"""
    return dt.strptime(datestr, '%Y-%m-%d')
