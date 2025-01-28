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
from src.common.utils.time import random_sleep
from src.common.utils.parsers import get_number_tiktok
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
            width=1280,
            height=800,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ):
        self.width = width
        self.height = height
        self.user_agent = user_agent
        self.page = None


    async def init(self, p):
        browser = await p.chromium.launch(headless=False)
        
        context = await browser.new_context(
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
        await self.page.goto(url, wait_until="networkidle")
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
        await random_sleep(0.33, 1.47)
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


    async def hover_and_get_views(self, video_element) -> str:
        """Given a video element, returns views text obtained"""
        await video_element.hover()
        await random_sleep(0.5, 1.7)
        #views = await self.page.locator()

        views = await video_element.evaluate("""
        (element) => {
            const viewElement = element.querySelector('strong[data-e2e="video-views"]');
            return viewElement ? viewElement.textContent.trim() : 'N/A';
        }
        """)
        return views


    async def get_video_count_and_videos(self) -> List[Dict]:
        """Gets all videos from a profile and its counts.
        """
        # TODO: Here check if a video is within a date window to be scraped again
        video_elements = await self.get_profile_video_elements()
        print(f"Video elements {len(video_elements)}")
        videos = []
        for element in video_elements:
            video_url = await element.evaluate('(el) => el.querySelector("a").href')
            # if the video was already processed do not do it again. (TODO: CHECK THIS)
            # if any(video_url['url'] == video_url for video in videos):
            #     continue
            views = await self.hover_and_get_views(element)
            videos.append({'url': video_url, 'views': views})
            
        print(f'Found {len(videos)} unique videos so far.')
        print(videos)
        return videos


    async def extract_video_info(self, url, get_comments_text = False) -> List[Dict]:
        """From video elements given returns data and if required all comments of the video
        """
        await self.page.goto(url, wait_until='networkidle')
        await random_sleep(2,5)
        await handle_captcha(self.page)

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
        video_info['shareCount'] = await self.page.locator(
            get_locator(locators['videos']['shareCount'])
        ).inner_text()
        video_info['savedCount'] = await self.page.locator(
            get_locator(locators['videos']['savedCount'])
        ).inner_text()
        video_info['description'] = await self.page.locator(
            get_locator(locators['videos']['description'])
        ).inner_text()
        video_info['date'] = await self.page.locator(
            get_locator(locators['videos']['date'])
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
        await self.load_profile_page(username)

        #1. Get general stats
        profile_data = await self.get_profile_basics(username)
        
        #2. Get videos and views data (check date to avoid duplication)
        profile_data['videos'] = await self.get_video_count_and_videos()
        return profile_data


    async def scrape_videos(self, profile_data: Dict, get_comments_text) -> Dict:
        """Iterates through all videos of the given profile and gets its
        data doing web scraping

        Parameters:
        profile_data (Dict): Profile data, can be obtained with self.scrape_profile_basics
        get_comments_text (bool): If true, it will scrape all comments in videos and obtain its contents
        """
        #3. Enter videos and get info (check date to avoid duplication)
        #  -  If get comments text is enabled scroll to comments and get info (check date!)
        for i, video in enumerate(profile_data['videos']):
            LOGGER.debug(f'Scraping video ({i}/{len(profile_data["videos"])}): {profile_data["videos"][i]["url"]}')
            try:
                profile_data['videos'][i] = await self.extract_video_info(video['url'])
                LOGGER.debug(f'Obtained: {profile_data["videos"][i]}')
            except Exception as E:
                LOGGER.error(f'Error getting video info: {E}')

            if get_comments_text:
                # TODO:
                print("Getting comments text")

        #4. Return videos info
        return profile_data

    def get_profile_total_counts(self, profile_data) -> Dict:
        """Given a profile data, it parses all numeric data of videos
        to get total counts.

        Parameters:
        profile_data (Dict): Profile data

        Returns (Dict)
        """
        counts = {}
        for i, video in enumerate(profile_data['videos']):
            if len(video['tags']) > 0:
                counts['hashtags'] = sum([
                    int(get_number_tiktok(len(video['tags'])))
                ])
            else:
                counts['hashtags'] = 0
            # TODO:
            # counts['hyperlinks'] =
            # TODO:
            #counts['short_videos'] = len()
            counts['likes_in_posts_got'] = sum([
                int(get_number_tiktok(likes)) for likes in video['likes']
            ])
            # TODO: mentions
            counts['saves_got'] = sum([
                int(get_number_tiktok(likes)) for likes in video['savedCount']
            ])
            counts['comments_got'] = sum([
                int(get_number_tiktok(likes)) for likes in video['commentCount']
            ])
            # counts['shares_got'] = sum([
            #     int(get_number_tiktok(likes) for likes in video['commentCount'])
            # ])
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
            profile_data['videos'][i] = await self.extract_video_info(video['url'])
            print("Video info obtained...")
            print(profile_data['videos'][i])

            if get_comments_text:
                # TODO:
                print("Getting comments text")

        #4. Return videos info
        return profile_data


