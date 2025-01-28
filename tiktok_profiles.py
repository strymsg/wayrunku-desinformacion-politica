"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
import asyncclick as click
from sqlalchemy.orm import sessionmaker
from src.db.db_manager import DbManager
from src.common.utils.parsers import get_number_tiktok
from src.tiktok.data_handlers.profiles import ProfilesDatahandler

from playwright.async_api import async_playwright
from src.tiktok.scraper.profile import TikTokProfileScraper

# ========== DB Connection and session ==========
db = DbManager.create()
engine = db.engine
Session = sessionmaker(bind=engine)
session = Session()
# ==============================================

@click.command()
@click.option("--from_file", "-f", default="",
              help="List of profile names separated file with new lines")
@click.option("--profiles", "-p", default="",
              help="List of profiles to scrape, sparated by commas. E.g.: @luchoxbolivia,@disasterpoii")
@click.option("--only_metadata", is_flag=True,
              help="To extract only metadata of the profile. Uses file profiles.csv as source and saves in out.csv")

async def scrape_profiles(from_file, profiles, only_metadata):
    
    # TODO: Incluir opciones
    profiles_to_scrape = []
    if profiles != '':
        for profile in profiles.split(','):
            print(profile)
            if profile.startswith("@"):
                profiles_to_scrape.append(profile[1:])
            else:
                profiles_to_scrape.append(profile)
            
        
    print(f"Profiles to get: {len(profiles_to_scrape)}: {profiles_to_scrape}")
    print()

    tiktok_profile_scraper = TikTokProfileScraper()


    async with async_playwright() as p:

        await tiktok_profile_scraper.init(p)
        
        for profile in profiles_to_scrape:
            print("Starting to scrape")
            print(f"============ {profile} ==============")
            print("=====================================")
            profile_data = await tiktok_profile_scraper.scrape_profile_basics(profile)
            # TODO: likes, video_plays, hashtags, hyperlinks, lives, short_videos.
            print("Basics:")
            print(profile_data)
            print()

            #profile_data = await tiktok_profile_scraper.scrape_profile(profile, only_metadata)

            profiles_dh = ProfilesDatahandler(session)

            registered = profiles_dh.upsert_for_today({
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

            # created = profiles_dh.insert({
            #     'name': profile_data['username'],
            #     'country_origin': 'unknown',
            #     'followers': int(get_number_tiktok(profile_data['followers_count'])),
            #     'following': int(get_number_tiktok(profile_data['following_count'])),
            #     'platform': 'tiktok',
            #     'url': profile_data['url'],
            #     'likes_got': int(get_number_tiktok(profile_data['likes_count'])),
            #     'saved_got': ...
            #     'posts': len(profile_data['videos']),
            #     'video_plays': sum([int(get_number_tiktok(video['views'])) for video in profile_data['videos']]),
            #     # TODO
            #     #'hashtags': profile_data[''],
            #     #'hiperlinks': profile_data[''],
            #     #'short_videos': profile_data[''],
            #     #'comments': profile_data[''],
            #     #'mentions':
            #     #'comments_got'
            #     #'lives'
            # })

            print(f" ...> Profile registered: {registered}")

            # TODO: Only scrape posts within the time from today set.
            
            profile_data = await tiktok_profile_scraper.scrape_videos(profile_data, False)
            total_counts = tiktok_profile_scraper.get_profile_total_counts(profile_data)

            # TODO: Get hyperlinks, video types and register posts in DB.
            registered = profiles_dh.upsert_for_today({
                'name': profile_data['username'],
                **total_counts
            })

            # ..
            # Once all done
            session.close()

if __name__ == '__main__':

    scrape_profiles(_anyio_backend="asyncio")
