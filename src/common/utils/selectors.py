"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
import logging

def get_selector_value(selector, *args):
    """Helps checking the selector value.
    Parameters:
    selector (str or function): If it is a function, uses args* to pass the function arguments and return
      a result. Else returns the selector string
    args (list): if `selector' is a function this args are passed as arguments to that function
    Returns:
    str: Resulting selector
    """
    svalue = ''
    if isinstance(selector['value'], str) is False:
        svalue = selector['value'](*args)
    else:
        svalue = selector['value']
    return svalue


def get_locator(selector, *args):
    """Replaces the selector values and returns a valid string to be used in
    playright page.locator"""
    svalue = get_selector_value(selector, *args)
    if selector['stype'] == 'xpath':
        svalue = f'xpath={svalue}'
    if selector['stype'] == 'css':
        svalue = f'css={svalue}'
    logging.info(f'  locator: {svalue}')
    return svalue
