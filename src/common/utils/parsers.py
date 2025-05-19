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


def facebook_date_text_parser(date_str) -> str:
    """Parses date presented by facebook and returns in format yyyy-mm-dd
    E.g.:
    - viernes, 2 de mayo de 2025 a las 5:36 pm --> 2025-05-02
    - domingo, 4 de mayo de 2025 a las 3:41 pm --> 2025-05-04
    """
    print(f'date_str: {date_str}')

    day = ''
    month_es = ''
    year = ''
    if date_str.find(',') != -1:
        date_part = date_str.split(" a las ")[0].split(", ")[1]
        # Split into day, Spanish month, and year
        day, month_es, year = date_part.split(" de ")
    else:
        day, month_es, year = date_str.split(" de ")

    # Dictionary to map Spanish months to English
    spanish_months = {
        'enero': 'January',
        'Febrero': 'February',
        'marzo': 'March',
        'abril': 'April',
        'mayo': 'May',
        'junio': 'June',
        'julio': 'July',
        'agosto': 'August',
        'septiembre': 'September',
        'octubre': 'October',
        'noviembre': 'November',
        'diciembre': 'December'
    }
    # Translate the Spanish month to English
    month_en = spanish_months[month_es.lower()]
    # Parse into a datetime object and format
    date_obj = dt.strptime(f"{day} {month_en} {year}", "%d %B %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date
    

def get_number_facebook(text) -> int:
    """Gets the number from text labeled
    E.g.:
    - 12 mil seguidores -> 12000
    - 851 seguidos -> 851
    """
    if not isinstance(text, str):
        return

    text = text.replace(u'\xa0', u' ')
    pattern = r"(?P<num>\d+[,|.]*\d*) ?(?P<escala>mil|mill.)* ?(?P<contando>seguidos|seguidores|comentarios|veces compartido])*"
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
    print(obtained)
    multiplier = 1
    if obtained['escala'] is None:
        return obtained['num']
    elif obtained['escala'] == 'mil':
        multiplier = 1000
    elif obtained['escala'] == 'mill.':
        multiplier = 1000000
    print(obtained['num'], multiplier)
    return str(int(float(obtained['num'].replace(',', '.'))*multiplier))


def get_unique_locators_for_post_attrs(aria_described_by: str, aria_labelledby: str) -> dict:
    """Returns a dictionary locators from props `aria_described_by' and
    `aria_labelledby'. E.g.:
    aria_described_by="«r1ea» «r1eb» «r1ec» «r1ee» «r1ed»"
    aria_labelledby="«r1bv»"
    Returns:
      {
        date: { css: "#«r1ea»"}, xpath: "*//[@id=«r1ea»"] },
        content_text: {css: "#«r1eb»", ... },
        content_media: "#«r1ec»",
        react_btn: "#«r1ee»",
        comment_count: "#«r1ed»", profile_name: "#«r1bv»"
      }
    """
    aria_described_by = aria_described_by.replace(u'\xa0', u' ')
    aria_labelledyby = aria_labelledby.replace(u'\xa0', u' ')
    
    pattern = r"(?P<date>«\w+»)\ (?P<content_text>«\w+»)\ (?P<content_media>«\w+»)\ (?P<react_btn>«\w+»)\ (?P<comment_count>«\w+»)"
    matches = list(re.finditer(pattern, aria_described_by))
    if len(matches) == 0:
        print(f"no match for '{aria_described_by}' with {pattern}")
        return text
    try:
        obtained = matches[0].groupdict()
    except Exception as E:
        print(f'not found capture group {E}')
        return text

    _dict = {
        'date': {
            'css': {
                'stype': 'css',
                'value': f"#{obtained.get('date', '')}",
                },
            'xpath': {
                'stype': 'xpath',
                'value': f"//*[@id='{obtained.get('date', '')}']"
            }
        },
        'content_text': {
            'css': {
                'stype': 'css',
                'value': f"#{obtained.get('content_text', '')}"
            },
            'xpath': {
                'stype': 'xpath',
                'value': f"//*[@id='{obtained.get('content_text', '')}']"
            }
        },
        'content_media': {
            'css': {
                'stype': 'css',
                'value': f"#{obtained.get('content_media', '')}",
                },
            'xpath': {
                'stype': 'xpath',
                'value': f"//*[@id='{obtained.get('content_media', '')}']"
            }
        },
        'react_btn': {
            'css': {
                'stype': 'css',
                'value': f"#{obtained.get('react_btn', '')}",
            },
            'xpath': {
                'stype': 'xpath',
                'value': f"//*[@id='{obtained.get('react_btn', '')}']"
            }
        },
        'comment_count': {
            'css': {
                'stype': 'css',
                'value': f"#{obtained.get('comment_count', '')}",
            },
            'xpath': {
                'stype': 'xpath',
                'value': f"//*[@id='{obtained.get('comment_count', '')}']"
            }
        }
    }

    text = aria_labelledby.split('«')[1]
    text = text.split('»')[0]
    _dict['profile_name'] = {
        'css': f'#{text}',
        'xpath': f'//*[@id="{text}"]'
    }
    return _dict
