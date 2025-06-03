"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
import asyncclick as click
import csv
import os

from sqlalchemy.orm import sessionmaker
from src.db.db_manager import DbManager
from src.common.utils.custom_logger import CustomLogger
from src.facebook.scraper.profile import FacebookProfileScraper
from src.facebook.data_handlers.profiles import ProfilesDatahandler
from src.facebook.data_handlers.posts import PostsDataHandler
from playwright.async_api import async_playwright
from src.common.utils.time import random_sleep, today_yyyymmdd, age_in_days, \
    datetime_from_yyyymmdd


LOGGER = CustomLogger('fb_profiles 🏃')

# TODO: parametrize these vars
MAX_POST_AGE = 7
MAX_POSTS = 30

# ========== DB Connection and session ==========
db = DbManager.create()
engine = db.engine
Session = sessionmaker(bind=engine)
session = Session()
# ==============================================


@click.command()
@click.option("--from_folder", "-f", default="data/facebook",
              help="Folder where to find csv files to get profiles. Expects columns 'Nombre' and 'Facebook' in each file.")
@click.option("--profiles", "-p", default="",
              help="List of profiles to scrape, spearated by comas. E.g: https://www.facebook.com/alejandracamargo1989,https://www.facebook.com/MarielaBaldiviesoDiputadaNacional")
@click.option("--login", "-l", is_flag=True,
              default=False,
              help="Does login process, otherwise uses saved context"
              )
async def scrape_profiles(from_folder, profiles, login):

    profiles_to_scrape = []
    # lista para ignorar perfiles
    to_ignore = [
        'Mauro Landivar ',
        'Maria Galindo',
        'Sayuri Loza',
        'ROSA TATIANA AÑEZ CARRASCO',
        'PAULA PAXI SUXO',
        'EVA LUZ HUMEREZ ALVEZ',
        'Jimena Antelo',
        'Rosario Callejas',
        'Nadia Montaño',
        'Roxana Pérez',
        'Coordinadora de la Mujer - Observatorio de Género BO',
        'Roxana Duchên',
        'Mamás Sororas de Bolivia ',
        'Angirü Bolivia ',
        'Carla Sandy Claure ',
        'Mueres Creando',
        'Por la vida de las mujeres',
        'Quya Reyna ',
        'Susana Bejarano',
        'Ciberwarmis - Mujeres ayudando a mujeres',
        'Natalia Aparicio',
        'MARIA BERTHA GUTIERREZ MENDOZA',
        'AZUCENA ALEJANDRA FUERTES MAMANI',
        'MARIA KHALINE MORENO CARDENAS',
        'Carola Antezana',
        'Laura Luisa Nayar',
        'ERICKA CHAVEZ AGUILERA',
        'Ana Lucía Velasco',
        'Cinthia Guidi',
        'LORENA ANAIZ PEREZ DAVALOS',
        'MAGDALENA MOGRO LACUNZA',
        'MARIA ESTHER GONGORA MIRANDA',
        'Nelly Flores',
        'Omarth Luna',
        'Wikimedistas de Bolivia',
        'Yessica Villarroel Caraballo',
        'LUCIANA MICHELLE CAMPERO CHAVEZ',
        'Luciana Campero',
        'La Pesada Subversiva ',
        'YHISSEL MARISOL DAVALO LANCEA',
        'Joshua Bellot',
        'ROSS MARY BRAVO SALAZAR',
        'El Confesionario UCB ',
        'Silvana Mucarzel',
        'Maria Rene Alvarez ',
        'María Patricia Arce',
        'Víctimas de Feminicidio e Infanticidio Bolivia ',
        'MARLENE FERNANDEZ MEJIAS',
        'CLAUDIA MALLON VARGAS',
        'SILVANA MUCARZEL DEMETRY',
        'FELIPA RAMOS MAMANI',
        'Jhanisse V. Daza',
        'Sofi Rocha',
        'YESENIA YARHUI ALBINO',
        'KARINA PATRICIA LIEBERS CACERES',
        'ELIANA RINA ACOSTA QUISPE',
        'Andrea Barrientos',
        'Jorge Copa',
        'MARILU EUGENIA RAMOS MAMANI',
        'Angirü Bolivia ',
    ]
    
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
                        if len(row['Nombre']) < 2 or len(row['Facebook']) < 10:
                            LOGGER.debug(f'Skipping {row["Nombre"]} incomplete data.')
                            continue

                        if 'ignorar' in reader.fieldnames:
                            if row['ignorar'] == 1:
                                continue

                        if row['Nombre'] in to_ignore:
                            continue

                        profiles_to_scrape.append({
                            'name': row['Nombre'],
                            'url': row['Facebook']
                        })
                        LOGGER.debug(f'Added: {row["Nombre"]}: {row["Facebook"]}.')
        # removing duplicates
        profiles_to_scrape = [dict(t) for t in {tuple(d.items()) for d in profiles_to_scrape}]
        LOGGER.info(f'\n\nTotal of {len(profiles_to_scrape)} profiles to scrape.\n : : : : : :')
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
                permissions=["clipboard-read", "clipboard-write"]
            )
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle")
            #await login(page)
            await random_sleep(84, 120)
            # Save storage state
            storage = await context.storage_state()
            with open("./fb_browser_state.json", "w") as f:
                f.write(str(storage))
            await browser.close()
    else:
        LOGGER.info("Using previous session avoiding to login.")
    

    facebook_profile_scraper = FacebookProfileScraper(max_days_age=MAX_POST_AGE,
                                                      max_posts=MAX_POSTS, max_fails=10)
    
    profiles_dh = ProfilesDatahandler(session)
    posts_dh = PostsDataHandler(session)
    
    
    async with async_playwright() as p:
        await facebook_profile_scraper.init(p)

        #### test insert

        # to_insert = {
        #     'name': 'Andrea Barrientos', 'url': 'https://www.facebook.com/AndreaBarrientosCC', 'following_count': 82, 'followers_count': 20000, 'creation_date': '2019-07-15',
        #     'id': '929', 'id_m_profile': '59', 'extraction_status': 'incomplete',
        #     'posts': [{'id_profile': '929', 'snapshot_date': '2025-05-16', 'creation_date': '2025-05-15', 'url': 'not-found-post-url-182271', 'content': 'José Luis Lupo se suma al binomio de la Unidad. Con amplia trayectoria en organismos internacionales, formación en economía y experiencia en resolución de crisis, nos a… Ver más', 'media_content': 'MMM', 'platform': 'facebook', 'likes_got': 40, 'comments_got': 25, 'shares': 4, 'react_like_got': 40, 'react_love_got': 6, 'react_haha_got': 32, 'react_sad_got': 0, 'react_wow_got': 0, 'react_angry_got': 1, 'react_icare_got': 0, 'extraction_status': 'completed'}]}
        # posts_registered = posts_dh.register_all_posts_from_profile(
        #     to_insert, MAX_POST_AGE
        # )
        # print(posts_registered)

        # import sys
        # sys.exit()

        ######

        for num_profile, profile in enumerate(profiles_to_scrape):
            LOGGER.info('\n ======================================== \n')
            LOGGER.info(f'Checking {profile["name"]}. ({num_profile}/{len(profiles_to_scrape)})\n\n')
            # searching in BD
            found_profile = profiles_dh.get_one_by(
                name=profile['name'],
                snapshot_date=today_yyyymmdd(),
                extraction_status='completed'
            )
            if found_profile is not None:
                LOGGER.info(f'  Profile "{profile}" was already processed today, skipping.')
                continue
            

            LOGGER.info(f"====== Starting to scrape '{profile['name']}' ==============")

            try:
                await facebook_profile_scraper.load_profile_page(profile['url'])
                await random_sleep(2, 4)

                profile_data = await facebook_profile_scraper.get_profile_basics(
                    profile['url'], profile['name'])
                # print(profile_basics)
                print(profile_data)

                profile_registered = profiles_dh.upsert_for_today({
                    'name': profile_data['name'],
                    'country_origin': 'unknown',
                    'creation_date': profile_data.get('creation_date', None),
                    'followers': int(profile_data['followers_count']),
                    'following': int(profile_data['following_count']),
                    'platform': 'facebook',
                    'url': profile_data['url'],
                    # TODO
                    #'hashtags': profile_data[''],
                    #'hiperlinks': profile_data[''],
                    #'short_videos': profile_data[''],
                    #'comments': profile_data[''],
                    #'mentions':
                    #'comments_got'
                    #'lives'
                })
                
                posts = await facebook_profile_scraper.scrape_entire_profile(
                    profile['url'], profile['name']
                )
                profile_data['posts'] = posts

                profile_data['id'] = profile_registered['id']
                profile_data['id_m_profile'] = profile_registered['id_m_profile']
                profile_data['extraction_status'] = profile_registered['extraction_status']
                profile_data['name'] = profile_registered['name']
                #print(posts)

                # registering posts to DB
                posts_registered = posts_dh.register_all_posts_from_profile(
                    profile_data, MAX_POST_AGE
                )
                profile_registered = profiles_dh.upsert_for_today({
                    'name': profile_data['name'],
                    'extraction_status': 'completed',
                })
                
                session.close()
                
            except Exception as e:
                LOGGER.error(f'Skipping scraping of profile {profile}.')
                LOGGER.error(LOGGER.format_exception(e))
            
    
if __name__ == '__main__':

    scrape_profiles(_anyio_backend='asyncio')
