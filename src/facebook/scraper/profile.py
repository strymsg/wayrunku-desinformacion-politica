"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import random
import traceback
import src.common.entity_tracker as EntityTracker

from src.facebook.scraper.locators import locators
from src.common.utils.pages import scroll_page
from src.common.utils.selectors import get_locator, get_selector_value, \
    get_text_from_page_and_locator, get_all_elements_from_locator, is_element_located
from src.common.utils.time import random_sleep, today_yyyymmdd, age_in_days, datetime_from_yyyymmdd
from src.common.utils.pages import scroll_page
from src.common.utils.custom_logger import CustomLogger
from src.common.utils.parsers import facebook_date_text_parser, get_number_facebook, \
    get_number_tiktok, get_unique_locators_for_post_attrs

from typing import List, Dict

LOGGER = CustomLogger('Facebook profile ⛏:')

class FacebookProfileScraper:
    """Class that helps scraping facebook profiles
    """

    def __init__(
            self,
            width=1420,
            height=980,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            max_days_age=7,
            max_posts=30,
            max_fails=10
    ):
        self.width = width
        self.height = height
        self.user_agent = user_agent
        self.max_days_age= max_days_age
        self.max_posts=max_posts
        self.max_fails=10
        self.page = None
        self.visited_posts = []


    async def init(self, p):
        browser = await p.chromium.launch(headless=False)

        # Load storage state from file
        with open("./fb_browser_state.json", "r") as f:
            storage = eval(f.readline())

        context = await browser.new_context(
            locale='en-US',
            viewport={'width': self.width, 'height': self.height},
            user_agent=self.user_agent,
            storage_state=storage
        )
        self.page = await context.new_page()


    async def load_profile_page(self, url: str):
        """Loads the profile using the url
        Parameters:
        p (async_playwright) Async playwrigth instance.
        """
        try:
            await self.page.goto(url, wait_until="networkidle", timeout=37000)
        except Exception as e:
            LOGGER.error(f'Error loading profile {url}')
            LOGGER.error(LOGGER.format_exception(e))
            raise e


    async def get_profile_basics(self, url, username):
        """Performs scraping to get basic data of the given profile.
        This basic data is followers, following...
        """
        profile_data = {
            'name': username,
            'url': url
        }

        # get profile general stats
        await random_sleep(0.43254, 2)
        text = await get_text_from_page_and_locator(
            self.page, locators['figure-profiles']['following-count'], throw_exception=False)
        profile_data['following_count'] = int(get_number_facebook(text)) if text != '' else 0
        text = await get_text_from_page_and_locator(
            self.page, locators['figure-profiles']['followers-count'], throw_exception=False)
        profile_data['followers_count'] = int(get_number_facebook(text)) if text != '' else 0

        # creation date
        await self.page.locator(
            get_locator(locators['profiles']['about-tab-by-name'], "Información")
        ).click()
        await random_sleep(0.53, 1.2)
        if await is_element_located(
                self.page, locators['figure-profiles']['profile-transparency-btn']) is False:
            return profile_data

        await self.page.locator(
            get_locator(locators['figure-profiles']['profile-transparency-btn']),
        ).click()
        text  = await get_text_from_page_and_locator(
            self.page, locators['figure-profiles']['creation-date'], throw_exception=False
        )
        profile_data['creation_date'] = facebook_date_text_parser(text) if text != '' else ''
        await self.page.locator(
            get_locator(locators['profiles']['about-tab-by-name'], 'Publicaciones')
        ).click()
        await random_sleep(0.54, 1.5)

        return profile_data
        

    def check_post_identifier(self, post_identifier):
        """Returns True if the given post is already in self.visited_posts"""
        return post_identifier in self.visited_posts


    async def get_next_post_locator(self, max_tries=10) -> str:
        """Searches for the next post to be visited by checking prop self.visited_posts
        The strategy is to scan the current posts reachable with the post container locator
        and take the first, gets its props (aria_described_by, aria_labelledby).
        If this props are in self.visited_posts, scrolls down and gets the next post
        to repeat this. Stops until a next 'free' post is obtained or max_tries is reached.

        Parameters:
        max_tries (int): Max number of posts to check before quiting

        Returns:
        (str): post locator in xpath format
        """
        LOGGER.debug('  Getting next post.')
        posts_visited = 0
        while posts_visited < max_tries:
            post_locators = self.page.locator(get_locator(locators['posts']['container-main']))
            post_elements = await post_locators.count()
            if post_elements > 1:
                for i in range(post_elements):
                    post_locator = post_locators.nth(i)
                    aria_described_by = await post_locator.get_attribute('aria-describedby')
                    aria_labelledby = await post_locator.get_attribute('aria-labelledby')

                    post_identifier = f'{aria_described_by} {aria_labelledby}'
                    if self.check_post_identifier(post_identifier) == True:
                        posts_visited += 1
                        continue
                    else: # post found
                        LOGGER.debug(f'Next post found {post_identifier}')
                        self.visited_posts.append(post_identifier)
                        return post_locator
                await scroll_page(self.page)
                await random_sleep(2.55, 4.29)
                posts_visited += 1
            elif post_elements == 1:
                post_locator = post_locators
                aria_described_by = await post_locator.get_attribute('aria-describedby')
                aria_labelledby = await post_locator.get_attribute('aria-labelledby')
                post_identifier = f'{aria_described_by} {aria_labelledby}'
                if self.check_post_identifier(post_identifier) == True:
                    posts_visited += 1
                    continue
                else: # post found
                    LOGGER.debug(f'Next post found {post_identifier}')
                    self.visited_posts.append(post_identifier)
                    return post_locator
            else:
                LOGGER.warning('Next post was not found.')
                return ''
        LOGGER.warning('Next post was not found.')
        return ''


    async def get_post_by_number(self, number=0, max_age=None) -> Dict:
        """Gets the profile post by the given number from latest to oldest,
        by default it only gets posts that are no older than self.max_age.

        Parameters:

        number (int): If given gets the number of post given as `number'. If not given gets the
        last post.
        max_age (int): Returns posts data that are no older than this in days. If not given
        will use `self.max_age' instead

        Returns:
        (Dict) With post data, if the post is older than `self.max_age' or given `max_age',
        it returns an empty dictionary.
        """
        # To navigate through posts it needs to first locate and scroll the next post.
        post_data = {}
        LOGGER.debug(f'Trying to get POST number {number}')

        await scroll_page(self.page)
        await random_sleep(2.11, 4.31)

        post_locator = await self.get_next_post_locator()

        aria_described_by = await post_locator.get_attribute('aria-describedby')
        aria_labelledby = await post_locator.get_attribute('aria-labelledby')
        locators_for_post = get_unique_locators_for_post_attrs(aria_described_by, aria_labelledby)

        # For Date it is better to hover on date text, then wait to a tooltip to appear
        LOGGER.debug('Getting: post-date')
        locator_built = get_locator(locators_for_post['date']['xpath'])
        locator_built += '//span[@class="x1rg5ohu x6ikm8r x10wlt62 x16dsc37 xt0b8zv"]'
        
        await self.page.locator(locator_built).wait_for()
        await self.page.locator(locator_built).hover()
        await random_sleep(2.07, 2.64)
        
        date_text_raw = await get_text_from_page_and_locator(
            self.page, locators['posts']['posted-date-text'], throw_exception=False)
        post_data['creation_date'] = facebook_date_text_parser(date_text_raw)

        # Check if date is no older than max_age
        max_age_in_days = max_age if max_age is not None else self.max_days_age
        post_age_in_days = age_in_days(datetime_from_yyyymmdd(post_data['creation_date']))
        LOGGER.debug(f'Post age {post_age_in_days}')
        if post_age_in_days > max_age_in_days:
            LOGGER.warning(f'This post is too old {post_age_in_days} (max {max_age_in_days}). Skipping.')
            return {}

        # url
        LOGGER.debug('Getting: url')
        post_data['url'] = ''
        try:
            comment_count_locator = self.page.locator(get_locator(locators_for_post['comment_count']['xpath']))
            print(comment_count_locator)
            await comment_count_locator.locator(
                get_locator(locators['posts']['share-btn-rel-to-comment'])).click()
            await random_sleep(0.82, 1.83)
            # after this click the modal closes
            await self.page.locator(get_locator(locators['posts']['copy-url'])).click()
            post_data['url'] = await self.page.evaluate_handle("navigator.clipboard.readText()").text
            print(f'URL: {post_data["url"]}, {str(post_data["url"])}')
        except Exception as e:
            LOGGER.warning('Could not retrieve URL for the post. (generating a random)')
            LOGGER.warning(LOGGER.format_exception(e))
            post_data['url'] = f'not-found-post-url-{random.randint(-550000, 550000)}'
        

        #locator_built += locators['posts']['share-btn-rel-to-comment']
        
        LOGGER.debug('Getting: content')
        post_data['content'] = await get_text_from_page_and_locator(
            self.page, locators_for_post['content_text']['xpath'], throw_exception=False)
        
        LOGGER.debug('Getting: reactions')
        if await is_element_located(self.page,
                locators_for_post['react_btn']['xpath']) is False:
            LOGGER.debug('No reactions found for this post.')
        else:
            await self.page.locator(get_locator(locators_for_post['react_btn']['xpath'])).click()
            await random_sleep(0.65, 1.66)
            post_data['react_like_got'] = await get_text_from_page_and_locator(
                self.page, locators['posts']['react-like-count'], throw_exception=False)
            print(post_data['react_like_got'])
            post_data['react_like_got'] = get_number_facebook(post_data['react_like_got'])

            post_data['react_love_got'] = await get_text_from_page_and_locator(
                self.page, locators['posts']['react-love-count'], throw_exception=False)
            print(post_data['react_love_got'])
            post_data['react_love_got'] = get_number_facebook(post_data['react_love_got'])

            post_data['react_sad_got'] = await get_text_from_page_and_locator(
                self.page, locators['posts']['react-sad-count'], throw_exception=False)
            print(post_data['react_sad_got'])
            post_data['react_sad_got'] = get_number_facebook(post_data['react_sad_got'])
            
            post_data['react_haha_got'] = await get_text_from_page_and_locator(
                self.page, locators['posts']['react-haha-count'], throw_exception=False)
            print(post_data['react_haha_got'])
            post_data['react_haha_got'] = get_number_facebook(post_data['react_haha_got'])
            
            post_data['react_wow_got'] = await get_text_from_page_and_locator(
                self.page, locators['posts']['react-wow-count'], throw_exception=False)
            post_data['react_wow_got'] = get_number_facebook(post_data['react_wow_got'])

            post_data['react_angry_got'] = await get_text_from_page_and_locator(
                self.page, locators['posts']['react-angry-count'], throw_exception=False)
            post_data['react_angry_got'] = get_number_facebook(post_data['react_angry_got'])

            post_data['react_icare_got'] = await get_text_from_page_and_locator(
                self.page, locators['posts']['react-icare-count'], throw_exception=False)
            post_data['react_icare_got'] = get_number_facebook(post_data['react_icare_got'])

            # TODO: Ver porque hacer click aqui falla en algunas ocasiones
            try:
                await self.page.locator(get_locator(locators['posts']['react-modal-close'])).wait_for(timeout=10000)
                await self.page.locator(
                    get_locator(locators['posts']['react-modal-close'])
                ).click()
            except Exception as e:
                LOGGER.debug('Error clicking to close react count.')
                

        LOGGER.debug('Getting: comments')
        post_data['comments_got'] = await get_text_from_page_and_locator(
            self.page, locators_for_post['comment_count']['xpath'], throw_exception=False)
        post_data['comments_got'] = get_number_facebook(post_data['comments_got'])
        
        # TODO: Check how to differentiate a post from repost
        post_data['post_type'] = 'post'

        LOGGER.debug('Getting: shares')
        post_data['shares'] = 0
        comment_locator = self.page.locator(
            get_locator(locators_for_post['comment_count']['xpath']))
        if await is_element_located(
                comment_locator,
                locators['posts']['share-count-rel-to-comment']) is False:
            LOGGER.debug('No shares found for this post.')
        else:
            text = await get_text_from_page_and_locator(
                comment_locator, locators['posts']['share-count-rel-to-comment'])
            post_data['shares'] = get_number_facebook(text)

        # TODO: See if content_media could be stored and to what end?
        LOGGER.debug('Getting: media content')
        post_data['media_content'] = ''
        # TODO: Fails when the locator fails
        # post_data['media_content'] = await get_text_from_page_and_locator(
        #     self.page, locators_for_post['media_content']['xpath'], throw_exception=False)

        return post_data


    async def scrape_entire_profile(self, url, username,
                                    get_comments_text = False) -> Dict:
        """Gets data from the entire profile of the given username from its url by scraping.

        Parameters:
        url(str): Url to the profile page
        username (str): Username or name of the profile
        get_comments_text (boolean): To implement
        """
        posts = []
        
        #await self.load_profile_page(url, username)
        #await random_sleep(3, 7)
        #profile_data = await self.get_profile_basics(url, username)

        post_number = 0
        fail_count = 0
        finished_posts = False
        while finished_posts is False and post_number < self.max_posts \
              and fail_count < self.max_fails:
            try:
                post = await self.get_post_by_number(post_number, self.max_days_age)
            
                if post.get('creation_date', None) is None:
                    LOGGER.debug(f'Finished to get Posts of max age {self.max_days_age}')
                    finished_posts = True
                else:
                    LOGGER.debug(f'Obtained post:\n{post}.')
                    posts.append(post)
                    post_number += 1
            except Exception as E:
                post_number += 1
                fail_count += 1
                LOGGER.error(f'Error getting post {post_number}\n {E}\n')
                LOGGER.error(f'Post errors: {fail_count}')

        LOGGER.debug(f'Obtained data from profile. Total of {len(posts)}.\n')
        LOGGER.debug(posts)

        return posts
