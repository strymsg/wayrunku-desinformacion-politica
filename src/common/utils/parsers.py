"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
import re

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
