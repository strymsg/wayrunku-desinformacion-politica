"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
import asyncclick as click
import csv
from sqlalchemy.orm import sessionmaker
from src.db.db_manager import DbManager
from src.common.utils.parsers import get_number_tiktok
from src.common.utils.time import today_yyyymmdd
from src.tiktok.data_handlers.profiles import ProfilesDatahandler
from src.tiktok.data_handlers.posts import PostsDataHandler
from src.common.utils.custom_logger import CustomLogger
from playwright.async_api import async_playwright
from src.tiktok.scraper.profile import TikTokProfileScraper


LOGGER = CustomLogger('tiktok_profiles 🏃')

# TODO: parametrize these vars
MAX_VIDEOS_PER_PROFILE = 20
MAX_DAYS_AGE_PER_VIDEO = 120


# ========== DB Connection and session ==========
db = DbManager.create()
engine = db.engine
Session = sessionmaker(bind=engine)
session = Session()
# ==============================================

@click.command()
@click.option("--from_file", "-f", default="",
              help="List csv file to get profiles. Expects columns 'Actor' and 'Pefil'")
@click.option("--profiles", "-p", default="",
              help="List of profiles to scrape, sparated by commas. E.g.: @luchoxbolivia,@disasterpoii")
@click.option("--only_metadata", is_flag=True,
              help="To extract only metadata of the profile. Uses file profiles.csv as source and saves in out.csv")

async def scrape_profiles(from_file, profiles, only_metadata):
    
    profiles_to_scrape = []
    if profiles != '':
        for profile in profiles.split(','):
            _profile = profile.replace('https://www.tiktok.com/', '').replace('@', '')
            profiles_to_scrape.append(_profile)
            LOGGER.debug(f'Added profile {_profile}')
    elif from_file != '':
        records = []
        with open(from_file, 'r', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                _profile = row['Perfil'].replace('https://www.tiktok.com/', '').replace('@', '')
                profiles_to_scrape.append(_profile)
                LOGGER.debug(f'Added profile {_profile}')
    LOGGER.debug(f"Profiles to get: {len(profiles_to_scrape)}: {profiles_to_scrape}")

    tiktok_profile_scraper = TikTokProfileScraper(
        max_videos=MAX_VIDEOS_PER_PROFILE,
        max_days_age=MAX_DAYS_AGE_PER_VIDEO
    )

    #### TEST #########
    # profile_test = {
    #     'videos': [
    #         {
    #             'url': 'https://www.tiktok.com/@moniquita1622/video/7446164565185875206', 'views': '6859',
    #             'likes': '13.8K',
    #             'commentCount': '306',
    #             'shareCount': '2125',
    #             'savedCount': '636',
    #             'description': '#agendapascualina #agendapascualina2025 #recuerdosadolescentes #nostalgia #pascualina',
    #             'date': '2024-12-8',
    #             'tags': ['#agendapascualina', '#agendapascualina2025', '#recuerdosadolescentes', '#nostalgia', '#pascualina']
    #         }, {'url': 'https://www.tiktok.com/@moniquita1622/video/7446147925593541893', 'views': '274.5K',
    #             'likes': '30', 'commentCount': '3', 'shareCount': 'Share', 'savedCount': '2', 'description': '#snow #bursaprovince', 'date': '2024-12-8', 'tags': ['#snow', '#bursaprovince']
    #             },
    #     ]
    # }
    # tc = tiktok_profile_scraper.get_profile_total_counts(profile_test)
    # print(tc)
    ###################

    profiles_dh = ProfilesDatahandler(session)
    posts_dh = PostsDataHandler(session)

    async with async_playwright() as p:

        # TODO: Parametrize max_videos
        await tiktok_profile_scraper.init(p)
        
        for profile in profiles_to_scrape:
            LOGGER.debug(f"Checking {profile} to scrape.")
            found_profile = profiles_dh.get_one_by(
                name=profile,
                snapshot_date=today_yyyymmdd(),
                extraction_status='completed'
            )
            if found_profile is not None:
                LOGGER.debug(f'  Profile "{profile}" was already processed today, skipping.')
                continue
            
            LOGGER.debug(f"====== Starting to scrape '{profile}' ==============")
            LOGGER.debug(f"======== Complete scraping = {only_metadata == False}========")


            try:
                profile_data = await tiktok_profile_scraper.scrape_profile_basics(profile)

                #profile_data = await tiktok_profile_scraper.scrape_profile(profile, only_metadata)

                profile_registered = profiles_dh.upsert_for_today({
                    'name': profile_data['username'],
                    'country_origin': 'unknown',
                    'followers': int(get_number_tiktok(profile_data['followers_count'])),
                    'following': int(get_number_tiktok(profile_data['following_count'])),
                    'platform': 'tiktok',
                    'url': profile_data['url'],
                    'likes_got': int(get_number_tiktok(profile_data['likes_count'])),
                    'posts': len(profile_data['videos']),
                    'video_plays': sum([int(get_number_tiktok(video['views'])) for video in profile_data['videos']]),
                    # TODO
                    #'hashtags': profile_data[''],
                    #'hiperlinks': profile_data[''],
                    #'short_videos': profile_data[''],
                    #'comments': profile_data[''],
                    #'mentions':
                    #'comments_got'
                    #'lives'
                })

                print(f" ...> Profile registered: {profile_registered}")

                # TODO: Only scrape posts within the time from today set.
            
                profile_data = await tiktok_profile_scraper.scrape_videos(profile_data, False)
                profile_data['id'] = profile_registered['id']
                profile_data['id_m_profile'] = profile_registered['id_m_profile']
                profile_data['extraction_status'] = profile_registered['extraction_status']
                profile_data['name'] = profile_registered['name']
                
                total_counts = tiktok_profile_scraper.get_profile_total_counts(profile_data)

                # TODO: Get hyperlinks, video types and register posts in DB.
                profile_registered = profiles_dh.upsert_for_today({
                    'name': profile_data['username'],
                    'extraction_status': 'completed',
                    **total_counts
                })

                # TODO: take 'only_metadata' flag into account

                # registering posts
                posts_registered = posts_dh.register_all_posts_from_profile(
                    profile_data, MAX_DAYS_AGE_PER_VIDEO)
                
                # ..
                # Once all done
                session.close()
            except Exception as e:
                LOGGER.error(f'Skipping scraping of profile {profile}.')
                LOGGER.error(LOGGER.format_exception(e))
                

if __name__ == '__main__':

    scrape_profiles(_anyio_backend="asyncio")
