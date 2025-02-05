"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import re
from datetime import datetime as dt
from datetime import timedelta

def get_number_tiktok(text):
    """Converts a text to number value
    Parameters:
    text (str): Text to convert e.g 2,3 mil seguidores

    Returns:
    (str) Number obtained
    """
    if not isinstance(text, str):
        return
    text = text.replace(u'\xa0', u' ')
    pattern = r"(?P<num>\d+[,|.]*\d*)(?P<escala>[K|M])*"    
    matches = list(re.finditer(pattern, text))
    if len(matches) == 0:
        print(f"no match for '{text}' with {pattern}")
        return text
    try:
        obtained = matches[0].groupdict()
    except Exception as E:
        print(f'not found capture group {E}')
        return text

    obtained['num'] = obtained['num'].replace(',', '.')

    multiplier = 1
    if obtained['escala'] is None:
        return obtained['num']
    elif obtained['escala'] == 'K':
        multiplier = 1000
    elif obtained['escala'] == 'M':
        multiplier = 1000000

    return str(int(float(obtained['num'].replace(',', '.'))*multiplier))


def tiktok_date_parser(date_str) -> str:
    """Parses date presented by tiktok and returns in format yyyymmdd
    E.g.:
    - 2024-8-8 --> 2024-08-08
    - 1-13 --> 2025-01-13  (Assuming current year 2025)
    - 1w ago -> 2025-01-22 (Assuming current date is 2025-01-29)
    - 2d ago -> 2025-01-28 (Assuming current date is 2025-01-29)
    - 5m ago -> 2025-01-29 (Assuming current date is 2025-01-29)
    - 4h ago -> 2025-01-29 (Assuming current date is 2025-01-29)
    - 2024-11 -> 2024-11-01
    """
    # note: \b\d{1,2}\b regex ensures only 1 to 2 digits strictly. Without \b can accidentally catch more
    patterns = {
        'yyyymmdd_re': r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})", # e.g. 2024-8-12
        'md_re': r"(?P<month>\b\d{1,2}\b)-(?P<day>\b\d{1,2}\b)", # e.g.: 1-13
        'nw_ago_re': r"(?P<weeks_ago>\d{1,2})w ago", # e.g.: 1w ago
        'nd_ago_re': r"(?P<days_ago>\d{1,2})d ago", # e.g.: 2d ago
        'nm_ago_re': r"(?P<mins_ago>\d{1,2})m ago", # e.g.: 5m ago
        'hm_ago_re': r"(?P<hours_ago>\d{1,2})h ago", # e.g.: 4h ago
        'yyyymm_re': r"(?P<year>\d{4})-(?P<month>\d{1,2})" # e.g.: 2024-11
    }
    date_str = date_str.replace(u'\xa0', u' ')

    pattern_match = None
    matches = None
    for pattern, regex in patterns.items():
        matches = list(re.finditer(regex, date_str))
        if len(matches) != 0:
            pattern_match = pattern
            break
        
    obtained = matches[0].groupdict()
    print(date_str, pattern_match, obtained)
    
    if pattern_match == 'yyyymmdd_re':
        date = dt(
            year=int(obtained['year']),
            month=int(obtained['month']),
            day=int(obtained['day'])
        )
    elif pattern_match == 'md_re':
        date = dt(year=dt.now().year,
                  month=int(obtained['month']),
                  day=int(obtained['day']))
    elif pattern_match == 'nw_ago_re':
        date = dt.now() - timedelta(weeks=int(obtained['weeks_ago']))
    elif pattern_match == 'nd_ago_re':
        date = dt.now() - timedelta(days=int(obtained['days_ago']))
    elif pattern_match == 'nm_ago_re':
        date = dt.now() - timedelta(minutes=int(obtained['mins_ago']))
    elif pattern_match == 'hm_ago_re':
        date = dt.now() - timedelta(hours=int(obtained['hours_ago']))
    elif pattern_match == 'yyyymm_re':
        date = dt(year=int(obtained['year']), month=int(obtained['month']), day=1)
    return dt.strftime(date, '%Y-%m-%d')

