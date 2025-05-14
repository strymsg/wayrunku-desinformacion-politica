"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import traceback
import src.common.entity_tracker as EntityTracker

from src.tiktok.scraper.locators import locators
from src.common.utils.pages import scroll_page
from src.tiktok.scraper.utils import handle_captcha
from src.common.utils.selectors import get_locator, get_selector_value
from src.common.utils.time import random_sleep, today_yyyymmdd, age_in_days, datetime_from_yyyymmdd
from src.common.utils.parsers import get_number_tiktok, tiktok_date_parser
from src.common.utils.custom_logger import CustomLogger

from typing import List, Dict

LOGGER = CustomLogger('Tiktok profile ⛏:')


class TikTokProfileScraper:
    """Class that helps scraping tik tok profiles"""
    profile: str
    url: str
    csv_input_file: str
    csv_output_file: str


    def __init__(
            self,
            max_videos=999999,
            max_days_age=99999,
            # width=1280,
            # height=800,
            width=1420,
            height=980,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ):
        self.width = width
        self.height = height
        self.user_agent = user_agent
        self.max_videos= max_videos
        self.max_days_age= max_days_age
        self.page = None


    async def init(self, p):
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            locale='en-US',
            viewport={'width': self.width, 'height': self.height},
            user_agent=self.user_agent,
        )
        self.page = await context.new_page()
        


    async def load_profile_page(self, username: str):
        """Loads the profile using username's url
        Parameters:
        p (async_playwright) Async playwrigth instance.
        """
        url = f"https://www.tiktok.com/@{username}"
        try:
            await self.page.goto(url, wait_until="networkidle")
        except Exception as e:
            LOGGER.error(f'Error loading profile {username}')
            LOGGER.error(LOGGER.format_exception(e))
            raise e
        await handle_captcha(self.page)
    

    async def get_profile_basics(self, username):
        """Performs scraping to get basic data of the given profile.
        This basic data is followers, following, likes and video counts
        """
        profile_data = {
            'username': username,
            'url': f"https://www.tiktok.com/@{username}"
        }

        # get profile general stats
        try:
            basics = await self.get_profile_counts_info()
            profile_data = { **profile_data, **basics }
            # TODO: Add logger
            LOGGER.info(f'Profile Info Obtained: {profile_data}')
        except Exception as E:
            profile_data['error'] = str(E) + '\n' + traceback.format_exc()
            LOGGER.error(f'Error while getting profile stats: {E}')
        return profile_data


    async def get_profile_counts_info(self) -> Dict:
        """Gets the profile general info from the current page instance
        """
        await random_sleep(0.33, 3.47)
        profile_info = {}
        print(self.page)
        print(type(self.page))
        profile_info['following_count'] = await self.page.locator(
            get_locator(locators['profiles']['followingCount'])
        ).inner_text()
        profile_info['followers_count'] = await self.page.locator(
            get_locator(locators['profiles']['followersCount'])
        ).inner_text()
        profile_info['likes_count'] = await self.page.locator(
            get_locator(locators['profiles']['likesCount'])
        ).inner_text()

        return profile_info
        
     
    async def get_profile_video_elements(self) -> List[Dict]:
        """Gets all visible video elements of the profile
        Note: To get all videos must scroll this until no new video is loaded
        """
        await scroll_page(self.page)
        await handle_captcha(self.page)
        elements = await self.page.locator(get_locator(locators['profiles']['videoElement'])).all()
        return elements


    async def get_pinned_video_elements(self) -> List[Dict]:
        """Gest all elements that have the pinned badge"""
        elements = await self.page.locator(get_locator(locators['videos']['pinnedBadge'])).all()
        return elements


    async def hover_and_get_views(self, video_element) -> str:
        """Given a video element, returns views text obtained"""
        await video_element.hover()
        await random_sleep(0.3, 1.1)
        #views = await self.page.locator()

        views = await video_element.evaluate("""
        (element) => {
            const viewElement = element.querySelector('strong[data-e2e="video-views"]');
            return viewElement ? viewElement.textContent.trim() : 'N/A';
        }
        """)
        return views


    async def get_video_count_and_videos(self) -> List[Dict]:
        """Gets all videos from a profile and its counts by scrolling the page. Also marks
        videos that are pinned.
        Gets a max of self.max_videos
        """
        await handle_captcha(self.page)

        videos = []
        last_video_count = 0
        no_new_videos_count = 0
        while True:
            await handle_captcha(self.page)

            pinned_video_elements = await self.get_pinned_video_elements()
            

            video_elements = await self.get_profile_video_elements()
            for i, element in enumerate(video_elements):
                video_url = await element.evaluate('(el) => el.querySelector("a").href')
                # if the video was already processed do not do it again. (TODO: CHECK THIS)
                if any(video['url'] == video_url for video in videos):
                    continue
                views = await self.hover_and_get_views(element)
                pinned = True if i <= len(pinned_video_elements) else False

                videos.append({
                    'url': video_url, 'views': views, 'pinned': pinned,
                    'element': element,
                })
                if len(videos) >= self.max_videos:
                    break
            LOGGER.debug(f'Found {len(videos)}  unique videos so far.')
            if len(videos) >= self.max_videos:
                break

            if len(videos) == last_video_count:
                no_new_videos_count += 1
            else:
                no_new_videos_count = 0

            last_video_count = len(videos)

            if no_new_videos_count >= 2:
                break
            await scroll_page(self.page)

                
        LOGGER.debug(f"Video elements {len(video_elements)} in total.")
        return videos[:self.max_videos-1]


    async def extract_video_info(self, url = None, get_comments_text = False) -> List[Dict]:
        """From video elements given returns data and if required all comments of the video

        Parameters:
        url (string): If given it goes to that url to load the video, if not it expects that
        the video page is already loaded.
        get_comments_text (boolean): Not implemented yet.
        """
        # TODO: add a parameter max_video_age to avoid scraping old videos

        if url is not None:
            await self.page.goto(url, wait_until='networkidle')
            await random_sleep(1.33, 4.25)
            await handle_captcha(self.page)

        view_more_btn_counts = await self.page.locator(
            get_locator(locators['videos']['viewMoreBtn'])
        ).count()
        if view_more_btn_counts > 0:
            await self.page.locator(
                get_locator(locators['videos']['viewMoreBtn'])
            ).click()

        video_info = {}
        # likes = self.page.locator(
        #     get_locator(locators['videos']['likeCount'])
        # )
        # print(likes)
        # print(await likes.inner_text())
        # video_info['likes'] = await likes.inner_text().strip()
        video_info['likes'] = await self.page.locator(
            get_locator(locators['videos']['likeCount'])
        ).inner_text()
        video_info['commentCount'] = await self.page.locator(
            get_locator(locators['videos']['commentCount'])
        ).inner_text()
        # video_info['shareCount'] = await self.page.locator(
        #     get_locator(locators['videos']['shareCount'])
        # ).inner_text()
        video_info['savedCount'] = await self.page.locator(
            get_locator(locators['videos']['savedCount'])
        ).inner_text()

        description_el_count = await self.page.locator(
            get_locator(locators['videos']['description'])
        ).count()
        video_info['description'] = ''
        if description_el_count > 0:
            if description_el_count == 1:
                video_info['description'] = await self.page.locator(
                    get_locator(locators['videos']['description'])
                ).inner_text()
            else:
                elements = await self.page.locator(
                    get_locator(locators['videos']['description'])
                ).all()
                text_desc = []
                for element in elements:
                    text_desc.append(await element.inner_text())
                    video_info['description'] = ','.join(text_desc)
        else:
            video_info['description'] = await self.page.locator(
                get_locator(locators['videos']['description-compactview'])
            ).inner_text()            

        date_el_count = await self.page.locator(get_locator(locators['videos']['date'])).count()
        if date_el_count > 0:
            video_info['date'] = await self.page.locator(
                get_locator(locators['videos']['date'])
            ).inner_text()
        else:
            video_info['date'] = await self.page.locator(
                get_locator(locators['videos']['date-compactview'])
            ).inner_text()            

        video_info['tags'] = []
        tags = await self.page.locator(get_locator(locators['videos']['tags'])).all()
        for tag_element in tags:
            tag = await tag_element.inner_text()
            video_info['tags'].append(tag)
        
        return video_info


    async def get_comments_full_data(self) -> List[Dict]:
        pass


    async def scrape_profile_basics(self, username: str) -> Dict:
        """Gets basic data information doing web scraping. Data includes:
        Basic profile stats, video counts

        Parameters:
        username (str): user name
        """
        try:
            await self.load_profile_page(username)
        except Exception as e:
            raise e

        #1. Get general stats
        profile_data = await self.get_profile_basics(username)
        
        #2. Get videos and views data (check date to avoid duplication)
        profile_data['videos'] = await self.get_video_count_and_videos()
        return profile_data

    
    async def scrape_videos(self, profile_data: Dict, get_comments_text) -> Dict:
        """Iterates through all videos of the given profile and gets its
        data doing web scraping. Also checks if videos are newer than max_days_age param
        and does this by checking every extracted video data, if it finds one video older
        than `self.max_days_age', stops checking the rmaining videos, this asumes videos are sorted
        by date.

        Parameters:
        profile_data (Dict): Profile data, can be obtained with self.scrape_profile_basics
        get_comments_text (bool): If true, it will scrape all comments in videos and obtain its contents

        Returns: Profile Data with video data in 'videos'. Automatically deletes older videos
        than `self.max_days_age'
        """
        #3. Enter videos and get info (check date to avoid duplication)
        #  -  If get comments text is enabled scroll to comments and get info (check date!)
        #  - Checking if videos are not too old.

        # Can happen that old
        
        last_video_index = 0
        done = False
        for i, video in enumerate(profile_data['videos']):
            LOGGER.debug(f'Scraping video ({i}/{len(profile_data["videos"])}): {profile_data["videos"][i]["url"]}  pinned: {profile_data["videos"][i]["pinned"]}')
            try:
                scraped_info = await self.extract_video_info(video['url'])
                
                video_age = age_in_days(
                    datetime_from_yyyymmdd(
                        tiktok_date_parser(scraped_info['date'])
                    ))
                LOGGER.debug(f'video age {video_age}')
                if video_age > self.max_days_age and video['pinned'] is False:
                    LOGGER.debug(f'Video date {scraped_info["date"]} is too old (max age: {self.max_days_age}). Skipping remaining videos.')
                    profile_data['videos'] = profile_data['videos'][:last_video_index]
                    done = True
                else:
                    profile_data['videos'][i] = {
                        **profile_data['videos'][i],
                        **scraped_info
                    }
                    LOGGER.debug(f'Obtained: {profile_data["videos"][i]}')
                    last_video_index = i
                    
            except Exception as e:
                LOGGER.error(f'Error getting video info: {e}')
                LOGGER.error(LOGGER.format_exception(e))

            if get_comments_text:
                # TODO:
                print("Getting comments text")

            if done:
                break

        #4. Return videos info
        return profile_data


    async def scrape_videos_by_clicking(self, profile_data: Dict, get_comments_text) -> Dict:
        """Iterates through all videos of the given profile and gets its
        data doing web scraping returning to the profile page and clicking to every video.

        Also checks if videos are newer than max_days_age param and does this by checking
        every extracted video data, if it finds one video older
        than `self.max_days_age', stops checking the rmaining videos, this asumes videos
        are sorted by date (this is default tiktok behavior).

        Parameters:
        profile_data (Dict): Profile data, can be obtained with self.scrape_profile_basics
        get_comments_text (bool): If true, it will scrape all comments in videos and obtain its contents

        Returns: Profile Data with video data in 'videos'. Automatically deletes older videos
        than `self.max_days_age'
        """
        last_video_index = 0
        done = False
        for i, video in enumerate(profile_data['videos']):
            LOGGER.debug(f'Scraping video ({i}/{len(profile_data["videos"])}): {profile_data["videos"][i]["url"]}  pinned: {profile_data["videos"][i]["pinned"]}')

            video_elements = await self.get_profile_video_elements()
            # clicking on the desired video
            LOGGER.debug('entering to the video...')
            await video_elements[i].click()
            await random_sleep(2.1, 5.2)
            try:
                scraped_info = await self.extract_video_info()
                video_age = age_in_days(
                    datetime_from_yyyymmdd(
                        tiktok_date_parser(scraped_info['date'])
                    ))
                LOGGER.debug(f'video age {video_age}')
                if video_age > self.max_days_age and video['pinned'] is False:
                    LOGGER.debug(f'Video date {scraped_info["date"]} is too old (max age: {self.max_days_age}). Skipping remaining videos.')
                    profile_data['videos'] = profile_data['videos'][:last_video_index]
                    done = True
                else:
                    profile_data['videos'][i] = {
                        **profile_data['videos'][i],
                        **scraped_info
                    }
                    LOGGER.debug(f'Obtained: {profile_data["videos"][i]}')
                    last_video_index = i
                    
            except Exception as e:
                LOGGER.error(f'Error getting video info: {e}')
                LOGGER.error(LOGGER.format_exception(e))
            
            if get_comments_text:
                # TODO:
                print("Getting comments text")

            if done:
                break

            await self.load_profile_page(profile_data['username'])
            
        return profile_data
            

    def get_profile_total_counts(self, profile_data) -> Dict:
        """Given a profile data, it parses all numeric data of videos
        to get total counts.

        Parameters:
        profile_data (Dict): Profile data

        Returns (Dict)
        """
        counts = {
            'hashtags': 0,
            'likes_in_posts_got': 0,
            'saves_got': 0,
            'comments_got': 0
        }
        for i, video in enumerate(profile_data['videos']):
            print(video)
            counts['hashtags'] += len(video.get('tags', []))
            # TODO
            # counts['hashtags_hyperlinks'] =
            # TODO:
            # counts['hyperlinks'] =
            # TODO:
            #counts['short_videos'] = len()
            counts['likes_in_posts_got'] += int(get_number_tiktok(video['likes']))
            # TODO: mentions
            counts['saves_got'] = (int(get_number_tiktok(video['savedCount'])))
            counts['comments_got'] = int(get_number_tiktok(video['commentCount']))
        return counts


    async def scrape_entire_profile(self, username, get_comments_text = False) -> Dict:
        """Gets full data of a profile doing web scraping

        Parameters:
        username (str): user name
        get_comments_text (bool): If true, it will scrape all comments in videos and obtain its contents
        """
        await self.load_profile_page(username)

        #1. Get general stats
        profile_data = await self.get_profile_basics(username)
        
        #2. Get videos and views data (check date to avoid duplication)
        profile_data['videos'] = await self.get_video_count_and_videos()
        
        #3. Enter videos and get info (check date to avoid duplication)
        #  -  If get comments text is enabled scroll to comments and get info (check date!)
        for i, video in enumerate(profile_data['videos']):
            print('CLICKING...')
            #profile_data['videos'][i] = await self.extract_video_info(video['url'])
            profile_data['videos'][i] = await self.scrape_videos_by_clicking()
            print("Video info obtained...")
            print(profile_data['videos'][i])

            if get_comments_text:
                # TODO:
                print("Getting comments text")

        #4. Return videos info
        return profile_data


