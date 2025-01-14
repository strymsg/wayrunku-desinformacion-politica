"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
from playwright.async_api import async_playwright
import asyncclick as click

import src.tiktok.scraper.profile as TikTokProfileScraper

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
            if profile.startswith("@"):
                profile = profile[1:]
            profiles_to_scrape.append(profile)
        
    print(f"Profiles to get: {len(profiles_to_scrape)}: {profiles_to_scrape}")
    print()

    async with async_playwright() as p:

        tiktok_profile_scraper = TikTokProfileScraper(p)

        for profile in profiles_to_scrape:
            print("Starting to scrape")
            print(f"============ {profile} ==============")
            print("=====================================")
            profile_data = await tiktok_profile_scraper.scrape_profile(p, profile, only_metadata)
            print(profile_data)
        

if __name__ == '__main__':
    scrape_profiles(_anyio_backend="asyncio")
