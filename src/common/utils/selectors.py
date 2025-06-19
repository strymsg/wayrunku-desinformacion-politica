"""
This is part of gobbo-datos
Copyright Rodrigo Garcia 2025
"""
from src.common.utils.custom_logger import CustomLogger
from src.common.utils.time import random_sleep
from src.common.utils.pages import scroll_down_pixels, scroll_up_pixels

LOGGER = CustomLogger('selectors 🧰:')

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
    LOGGER.debug(f'  locator: {svalue}')
    return svalue


async def is_element_located(page, selector, *args):
    """Tries to get the element from the given selector on the given page obeject.
    If element is not located or visible returns False
    """
    element = page.locator(get_locator(selector, *args))
    if await element.count() > 0:
        return True
    return False
    

async def get_all_elements_from_locator(page, selector, throw_exception=True, *args):
    """Returns all the elements for the given page and locator

    Parameters:
    page (Page Object playwrigth): Page object from browser context to search in
    locator: locator string
    throw_exception (bool): If true, raises an exception when no element for the given
      locator is found, otherwise will return an empty list
    args (Arg list): Additional args list for the selector

    Returns:
    List of Web elements found
    """
    try:
        return await page.locator(get_locator(selector, *args)).all()
    except Exception as e:
        if not throw_exception:
            LOGGER.warn(f'Not able to get elements with selector {selector}')
            return []
        LOGGER.error(f'Error getting elements with selector {selector}')
        LOGGER.error(LOGGER.format_exception(e))
        raise e

async def scroll_until_element_found(page, locator, max_attempts=3, throw_exception=True,
                                     scroll_back=True):
    """Tries to scroll into view to an element given the locator by attempting
    to scroll down a given number of times.

    Parameters:
    p (Page Object playwrigth): Page object from browser context to search in
    locator: locator string
    max_attempts (int): Max number of attempts to scroll down
    throw_exception (bool): If true, raises an exception when no element for the given
      locator is found, otherwise will return an empty string
    scroll_back (bool): If true scrolls back to return when the element is not found
    """
    LOGGER.debug(f'(v) Scrolling until element found {locator} max. {max_attempts}')
    for _ in range(max_attempts):
        try:
            # Check if the element exists
            print(f'scroll to::::: {locator}')
            await page.locator(locator).wait_for(timeout=2000)
            await page.locator(locator).scroll_into_view_if_needed()
            return page.locator(locator)
        except Exception as e:
            # Scroll down the page
            LOGGER.warn(e)
            LOGGER.debug('Element not found, scrolling...')
            await scroll_down_pixels(page, 200)
            await random_sleep(0.8, 1.2) # wait for content to load
    if scroll_back is True:
        LOGGER.debug(f'Scrolling back {200*max_attempts} pixels.')
        for i in range(max_attempts):
            await scroll_up_pixels(page, 200)

    if throw_exception is True:
        raise Exception("Element not found after maximum scroll attempts")

    LOGGER.warning(f'Element was not found after {max_attempts} scroll attempts')
    

async def get_text_from_all_elements(self, locator, *args):
    """Gets the text from all elements that matches the locator.
       When there are multiple elements the text is concat with ,
        If no element is found returns an empty string
    """
    text = ''
    if await is_element_located(self.page, locator):
        web_elements =  await self.page.locator(get_locator(locator, *args)).all()
        if len(web_elements) == 1:
            return await web_elements[0].inner_text()
        
        for web_element in web_elements:
            text += await web_element.inner_text() + ','
    return text


async def get_text_from_page_and_locator(p, locator: str, throw_exception=True,
                                         timeout=1500):
    """Returns the `inner_text' from the element find with the given locator

    Parameters:
    p (Page Object playwrigth): Page object from browser context to search in
    locator: locator string
    throw_exception (bool): If true, raises an exception when no element for the given
      locator is found, otherwise will return an empty string
    """
    try:
        txt = await p.locator(get_locator(locator)).inner_text(timeout=timeout)
        print(f' -- text obtained --: {txt}')
        return txt if txt is not None else ''
    except Exception as e:
        LOGGER.debug(f'Could not get element with locator: {locator}')
        LOGGER.debug(e)
        #LOGGER.debug(f'\n{LOGGER.format_exception(e)}\n- - - - err. getting text - - - - - -\n')
        if throw_exception is False:
            return ''
        raise e


async def highlight_element_by_page_and_locator(p, locator):
    """Changes the element to highlight its borders so can be seen

    Parameters:
    p (Page Object playwrigth): Page object from browser context to search in
    locator: locator string
    """
    LOGGER.debug(f'Highlight element: {locator}')
    try:
        # Wait for element to be present
        element = await p.wait_for_selector(locator, timeout=5000)
        
        # Add border style via JavaScript evaluation
        await element.evaluate(
            "element => element.style.border = arguments[0]",
            "4px dashed #02FF02"
        )
        # Optional: Add screenshot for visual confirmation
        #await p.screenshot(path="highlighted_element.png")
        await random_sleep(0.4, 0.7)
        return True
    except Exception as e:
        LOGGER.warn(f"Highlight failed: {str(e)}")
        return False


async def highlight_element_in_page(p, element):
    """Changes the element to highlight its borders so can be seen

    Parameters:
    p (Page Object playwrigth): Page object from browser context to search in
    element (Playwright element): element to highlight
    """
    LOGGER.debug(f'Highlight element: {element}')
    try:
        # Add border style via JavaScript evaluation
        await element.evaluate(
            "(element, border_style) => {"
            "   element.style.border = border_style;"
            "   return element.getBoundingClientRect();"  # Forces re-render
            "}",
            '4px dashed #02FF02' # border applied
        )        
        # Optional: Add screenshot for visual confirmation
        #await p.screenshot(path="highlighted_element.png")
        await random_sleep(0.4, 0.7)
        return True
    except Exception as e:
        LOGGER.warn(f"Highlight failed: {str(e)}")
        return False
    
