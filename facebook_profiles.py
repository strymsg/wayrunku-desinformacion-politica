"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
import asyncclick as click
import csv
import os

from src.common.utils.custom_logger import CustomLogger
from src.facebook.scraper.profile import FacebookProfileScraper
from playwright.async_api import async_playwright
from src.common.utils.time import random_sleep, today_yyyymmdd, age_in_days, datetime_from_yyyymmdd


LOGGER = CustomLogger('fb_profiles 🏃')


@click.command()
@click.option("--from_folder", "-f", default="",
              help="Folder where to find csv files to get profiles. Expects columns 'Nombre' and 'Facebook' in each file.")
@click.option("--profiles", "-p", default="",
              help="List of profiles to scrape, spearated by comas. E.g: https://www.facebook.com/alejandracamargo1989,https://www.facebook.com/MarielaBaldiviesoDiputadaNacional")
@click.option("--login", "-l", is_flag=True,
              default=False,
              help="Does login process, otherwise uses saved context"
              )
async def scrape_profiles(from_folder, profiles, login):

    profiles_to_scrape = []
    if profiles != '':
        profiles_to_scrape = profiles.split(',')
    elif from_folder != '':
        records = []
        for root, dirs, files in os.walk(from_folder):
            for file in files:
                if file.endswith(".csv") is False:
                    continue
                _file = os.path.join(from_folder, file)
                LOGGER.info(f"\n------------ Checking File {_file} ------------")
                with open(_file, 'r', encoding='UTF-8', newline='') as csv_file:
                    reader = csv.DictReader(csv_file)
                    print(reader.fieldnames)
                    if reader.fieldnames is None or \
                       'Nombre' not in reader.fieldnames or 'Facebook' not in reader.fieldnames:
                        LOGGER.debug(f'Skipping {file}, does not have needed columns.')
                        continue
                    for row in reader:
                        profiles_to_scrape.append({
                            'name': row['Nombre'],
                            'url': row['Facebook']
                        })
                        LOGGER.debug(f'Added: {row["Nombre"]}: {row["Facebook"]}.')
    if login:
        LOGGER.info("DO LOGIN")
        # TODO: Login

        async with async_playwright() as p:
            url = "https://www.facebook.com"
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 1284, 'height': 722},
                #user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            )
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle")
            #await login(page)
            await random_sleep(50, 80)
            # Save storage state
            storage = await context.storage_state()
            with open("./fb_browser_state.json", "w") as f:
                f.write(str(storage))
            await browser.close()
    else:
        LOGGER.info("Using previous session avoiding to login.")
    

    facebook_profile_scraper = FacebookProfileScraper(max_days_age=7, max_posts=30, max_fails=10)
    

    async with async_playwright() as p:
        await facebook_profile_scraper.init(p)

        for num_profile, profile in enumerate(profiles_to_scrape):
            LOGGER.info('\n ======================================== \n')
            LOGGER.info(f'Checking {profile["name"]}. ({num_profile}/{len(profiles_to_scrape)})\n\n')
            # TODO: search in BD

            LOGGER.info(f"====== Starting to scrape '{profile['name']}' ==============")

            try:
                await facebook_profile_scraper.load_profile_page(profile['url'])
                await random_sleep(4, 8)
            
                # TODO: get profile basics
                profile_basics = await facebook_profile_scraper.get_profile_basics(
                    profile['url'], profile['name'])

                print(profile_basics)
                # TODO: check if profile needs to be inserted or updated for today
                
                # TODO: get posts
                posts = await facebook_profile_scraper.scrape_entire_profile(
                    profile['url'], profile['name']
                )
                print(posts)
                # TODO: process data to insert/update in BD
                
            except Exception as e:
                LOGGER.error(f'Skipping scraping of profile {profile}.')
                LOGGER.error(LOGGER.format_exception(e))
            
    
if __name__ == '__main__':

    scrape_profiles(_anyio_backend='asyncio')
