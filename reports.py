"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import os
import click
import csv
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import insert, select, update, func
from sqlalchemy import text

from src.db.db_manager import DbManager
from src.common.utils.custom_logger import CustomLogger
from src.common.utils.csv import csv_write_headers
from src.common.utils.time import today_yyyymmdd


LOGGER = CustomLogger('Reports ⛁:')


db = DbManager.create()
engine = db.engine


DESTINY_FOLDER='./data/reports/'

SNAPSHOT_DATE_FROM = '2025-07-29'
SNAPSHOT_DATE_TO = '2025-07-30'

@click.command()
@click.option(
    "--from-date", default=SNAPSHOT_DATE_FROM,
    help="Start Report from this snapshot_date. Format YYYY-MM-DD. E.g.: 2025-05-22")
@click.option(
    "--to-date", default=SNAPSHOT_DATE_TO,
    help="End date Report until this snapshot_date. Format YYYY-MM-DD. E.g.: 2025-05-23")
def do_reports(from_date, to_date):

    with engine.connect() as conn:

        # ====== Reporte de resumen (facebook)
        # Todos los posts por perfil monitoreado con resumenes dado un rango de fechas

        query = text(f"""
WITH latest_profile AS (
    SELECT DISTINCT ON (id_m_profile)
        id_m_profile,
        name,
        followers,
        following,
        platform
    FROM profiles
        where platform = 'facebook'
	   and snapshot_date >= '{SNAPSHOT_DATE_FROM}'
           and snapshot_date <= '{SNAPSHOT_DATE_TO}'
    ORDER BY id_m_profile, snapshot_date desc
),
post_totals AS (
    SELECT
        p.id_m_profile,
	COUNT(*) as "posts publicados",
	SUM(pst.comments_got) as "comentarios obtenidos",
	SUM(pst.shares) as "posts compartidos", 
	SUM(pst.likes_got) as "me gusta", SUM(pst.react_love_got) as "me encanta",
	SUM(pst.react_haha_got) as "me divierte", SUM(pst.react_sad_got) as "me entristece",
	SUM(pst.react_angry_got) as "me enoja", SUM(pst.react_wow_got) as "me sorprende",
	SUM(pst.react_icare_got) as "me importa",
	SUM(pst.total_reactions) as "reacciones en total"
    FROM posts pst
    JOIN profiles p ON pst.id_profile = p.id
    where pst.platform = 'facebook'
       and pst.snapshot_date >= '{SNAPSHOT_DATE_FROM}'
       and pst.snapshot_date <= '{SNAPSHOT_DATE_TO}'
    GROUP BY p.id_m_profile
)
SELECT 
    mp.name,
    COALESCE(pt."posts publicados", 0) as "posts publicados",
    COALESCE(lp.followers, 0) AS "seguidores",
    COALESCE(lp.following, 0) AS "siguiendo",
    coalesce(pt."comentarios obtenidos", 0) as "comentarios obtenidos",
    COALESCE(pt."posts compartidos", 0) AS "posts compartidos",
    COALESCE(pt."me gusta", 0) AS "me gusta",
    COALESCE(pt."me encanta", 0) AS "me encanta",
    COALESCE(pt."me divierte", 0) AS "me divierte",
    COALESCE(pt."me entristece", 0) AS "me entristece",
    COALESCE(pt."me enoja", 0) AS "me enoja",
    COALESCE(pt."me sorprende", 0) AS "me sorprende",
    COALESCE(pt."me importa", 0) AS "me importa",
    COALESCE(pt."reacciones en total", 0) as "reacciones en total",
    (case when mp.is_candidate = 1 then 'sí' else 'no' end)
    	  as "candidato identificado",
    mp.url as "url del perfil",
    mp.creation_date as "creación de perfil"
FROM m_profile mp
LEFT JOIN latest_profile lp ON mp.id = lp.id_m_profile
LEFT JOIN post_totals pt ON mp.id = pt.id_m_profile
where lp.platform = 'facebook'
	and lp.id_m_profile = pt.id_m_profile
order by COALESCE(pt."posts publicados", 0) desc;
    """)

        LOGGER.debug("Starting report 1 (summary for each profile Facebook)")
        LOGGER.debug(f"  SQL query:\n{query}\n")
        
        results = conn.execute(query)

        headers = []
        rows_to_save = []
        for record in results:
            if len(rows_to_save) == 0:
                headers = [key for key in record._asdict().keys()]
            LOGGER.debug(record._asdict())
            rows_to_save.append([value for value in record._asdict().values()])

        filename = f'{DESTINY_FOLDER}summaries/fb_{today_yyyymmdd()}.csv'
        LOGGER.debug(f'Writing to csv. {filename}')
        # Escribiendo como csv
        csv_write_headers(filename=filename,
                          headers=headers, replace_file=True)

        with open(filename, 'a', encoding='UTF-8', newline='') as f:
            writer = csv.writer(f)
            for row in rows_to_save:
                writer.writerow(row)
        LOGGER.info(f'Report saved {filename} ({len(rows_to_save)} rows.)')

        # ======== Reporte de posts por perfil
        # Los posts de cada perfil monitoreado dado un rango de fechas

        query = text(f"""
        select mp."name" as "nombre perfil" , mp.url as "url perfil",
	  (case when mp.is_candidate = 1 then 'sí' else 'no' end) as "candidato identificado",        	    prof.creation_date as "creación del perfil",
	  prof.followers as "seguidores" , prof."following" as "seguidos",
	  p.creation_date as "fecha post",
	  p.post_type as "tipo de post",
	  p.url as "url post", p.shares as "comparticiones",
          p.comments_got as "comentarios",
	  p.total_reactions as "reacciones en total",
	  p.react_like_got as "me gusta", p.react_love_got as "me encanta",
	  p.react_haha_got as "me divierte", p.react_sad_got as "me entristece",
	  p.react_wow_got as "me sorprende", p.react_angry_got as "me enoja",
	  p.react_icare_got as "me importa",
	  p."content" as "contenido"
          from posts p
          inner join profiles prof ON prof.id = p.id_profile 
          inner join m_profile mp on mp.id = prof.id_m_profile 
          where p.platform = 'facebook'
            and p.snapshot_date >= '{SNAPSHOT_DATE_FROM}'
            and p.snapshot_date <= '{SNAPSHOT_DATE_TO}'
          order by  mp."name", p.creation_date
        """)

        LOGGER.debug("Starting report 2 (posts per each profile Facebook)")
        LOGGER.debug(f"  SQL query:\n{query}\n")

        results = conn.execute(query)

        headers = []
        to_save = {}
        for record in results:
            dict = record._asdict()
            if len(headers) == 0:
                headers = [key for key in record._asdict().keys()]
            
            LOGGER.debug(record._asdict())

            profile = record._asdict()['nombre perfil']
            
            if to_save.get(profile, None) is None:
                to_save[profile] = {
                    'filename': f'{DESTINY_FOLDER}individuals/{profile}/fb_{profile}_{today_yyyymmdd()}.csv',
                    'rows': []
                }
            to_save[profile]['rows'].append([value for value in record._asdict().values()])
            
        # Agregando al csv correspondiente
        for profile, record in to_save.items():
            os.makedirs(os.path.dirname(record['filename']), exist_ok=True)
            csv_write_headers(filename=record['filename'], headers=headers, replace_file=True)

            with open(record['filename'], 'a', encoding='UTF-8', newline='') as f:
                writer = csv.writer(f)
                for row in record['rows']:
                    writer.writerow(row)
            LOGGER.info(f'Report saved {record["filename"]} ({len(record["rows"])})')


        # ====== Reporte acumulado resumen (facebook)
        # Todos los posts por perfil monitoreado con resumenes del 2025

        query = text(f"""
        WITH latest_profile AS (
            SELECT DISTINCT ON (id_m_profile)
                id_m_profile,
                name,
                followers,
                following,
                platform
            FROM profiles
                where platform = 'facebook'
        			and snapshot_date >= '2025-01-01' and snapshot_date <= '2025-12-31'
            ORDER BY id_m_profile, snapshot_date desc
        ),
        post_totals AS (
            SELECT
                p.id_m_profile,
        	COUNT(*) as "posts publicados",
        	SUM(pst.comments_got) as "comentarios obtenidos",
        	SUM(pst.shares) as "posts compartidos", 
        	SUM(pst.likes_got) as "me gusta", SUM(pst.react_love_got) as "me encanta",
        	SUM(pst.react_haha_got) as "me divierte", SUM(pst.react_sad_got) as "me entristece",
        	SUM(pst.react_angry_got) as "me enoja", SUM(pst.react_wow_got) as "me sorprende",
        	SUM(pst.react_icare_got) as "me importa",
        	SUM(pst.total_reactions) as "reacciones en total"
            FROM posts pst
            JOIN profiles p ON pst.id_profile = p.id
            where pst.platform = 'facebook'
        		and pst.snapshot_date >= '2025-01-01' and pst.snapshot_date <= '2025-12-31'
            GROUP BY p.id_m_profile
        )
        SELECT 
            mp.name,
            COALESCE(pt."posts publicados", 0) as "posts publicados",
            COALESCE(lp.followers, 0) AS "seguidores",
            COALESCE(lp.following, 0) AS "siguiendo",
            coalesce(pt."comentarios obtenidos", 0) as "comentarios obtenidos",
            COALESCE(pt."posts compartidos", 0) AS "posts compartidos",
            COALESCE(pt."me gusta", 0) AS "me gusta",
            COALESCE(pt."me encanta", 0) AS "me encanta",
            COALESCE(pt."me divierte", 0) AS "me divierte",
            COALESCE(pt."me entristece", 0) AS "me entristece",
            COALESCE(pt."me enoja", 0) AS "me enoja",
            COALESCE(pt."me sorprende", 0) AS "me sorprende",
            COALESCE(pt."me importa", 0) AS "me importa",
            COALESCE(pt."reacciones en total", 0) as "reacciones en total",
            (case when mp.is_candidate = 1 then 'sí' else 'no' end)
            	  as "candidato identificado",
            mp.url as "url del perfil",
            mp.creation_date as "creación de perfil"
        FROM m_profile mp
        LEFT JOIN latest_profile lp ON mp.id = lp.id_m_profile
        LEFT JOIN post_totals pt ON mp.id = pt.id_m_profile
        where lp.platform = 'facebook'
        	and lp.id_m_profile = pt.id_m_profile
        order by COALESCE(pt."posts publicados", 0) desc;
        """)

        LOGGER.debug("Starting report 3 (Accumulated report for Facebook)")
        LOGGER.debug(f"  SQL query:\n{query}\n")
        
        results = conn.execute(query)

        headers = []
        rows_to_save = []
        for record in results:
            if len(rows_to_save) == 0:
                headers = [key for key in record._asdict().keys()]
            LOGGER.debug(record._asdict())
            rows_to_save.append([value for value in record._asdict().values()])

        filename = f'{DESTINY_FOLDER}summaries/fb_acumulado_hasta_{today_yyyymmdd()}.csv'
        LOGGER.debug(f'Writing to csv. {filename}')
        # Escribiendo como csv
        csv_write_headers(filename=filename,
                          headers=headers, replace_file=True)

        with open(filename, 'a', encoding='UTF-8', newline='') as f:
            writer = csv.writer(f)
            for row in rows_to_save:
                writer.writerow(row)
        LOGGER.info(f'Report saved {filename} ({len(rows_to_save)} rows.)')


        # ======== Reporte de todos los posts por perfil
        #  Los posts de cada perfil monitoreado dado un rango de fechas

        query = text(f"""
        select mp."name" as "nombre perfil" , mp.url as "url perfil",
	  p.snapshot_date,
	  prof.creation_date as "creación del perfil",
	  (case when mp.is_candidate = 1 then 'sí' else 'no' end) as "candidato identificado",
	  prof.followers as "seguidores" , prof."following" as "seguidos",
	  p.creation_date as "fecha post",
	  p.post_type as "tipo de post",
	  p.url as "url post", p.shares as "comparticiones",
	  p.comments_got  as "comentarios",
	  p.total_reactions as "reacciones en total",
	  p.react_like_got as "me gusta", p.react_love_got as "me encanta",
	  p.react_haha_got as "me divierte", p.react_sad_got as "me entristece",
	  p.react_wow_got as "me sorprende", p.react_angry_got as "me enoja",
	  p.react_icare_got as "me importa",
	  p."content" as "contenido"
        from posts p
          inner join profiles prof ON prof.id = p.id_profile 
          inner join m_profile mp on mp.id = prof.id_m_profile 
        where p.platform = 'facebook'
          and p.snapshot_date >= '2025-01-01'
          and p.snapshot_date <= '2025-12-31'
        order by  mp."name", p.creation_date
        """)

        LOGGER.debug("Starting report 4 (All posts per each profile Facebook)")
        LOGGER.debug(f"  SQL query:\n{query}\n")

        results = conn.execute(query)

        headers = []
        to_save = {}
        for record in results:
            dict = record._asdict()
            if len(headers) == 0:
                headers = [key for key in record._asdict().keys()]
            
            LOGGER.debug(record._asdict())

            profile = record._asdict()['nombre perfil']
            
            if to_save.get(profile, None) is None:
                to_save[profile] = {
                    'filename': f'{DESTINY_FOLDER}individuals/acumulados/{profile}/fb_posts_acumulados_{profile}.csv',
                    'rows': []
                }
            to_save[profile]['rows'].append([value for value in record._asdict().values()])
            
        # Agregando al csv correspondiente
        for profile, record in to_save.items():
            os.makedirs(os.path.dirname(record['filename']), exist_ok=True)
            csv_write_headers(filename=record['filename'], headers=headers, replace_file=True)

            with open(record['filename'], 'a', encoding='UTF-8', newline='') as f:
                writer = csv.writer(f)
                for row in record['rows']:
                    writer.writerow(row)
            LOGGER.info(f'Report saved {record["filename"]} ({len(record["rows"])})')
            
if __name__ == '__main__':
    do_reports()
