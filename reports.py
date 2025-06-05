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

SNAPSHOT_DATE_FROM = '2025-06-02'
SNAPSHOT_DATE_TO = '2025-06-03'

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
    select mp.name, p.snapshot_date,
    COUNT(*) as "posts publicados",
	SUM(prof.followers) as "seguidores", SUM(prof."following") as "siguiendo", 
	SUM(p.comments_got) as "comentarios",
	SUM(p.shares) as "posts compartidos", 
	SUM(p.likes_got) as "me gusta", SUM(p.react_love_got) as "me encanta",
	SUM(p.react_haha_got) as "me divierte", SUM(p.react_sad_got) as "me entristece",
	SUM(p.react_angry_got) as "me enoja", SUM(p.react_wow_got) as "me sorprende",
	SUM(p.react_icare_got) as "me importa",
        SUM(p.total_reactions) as "reacciones en total",
	mp.url 
    from posts p
    inner join profiles prof ON prof.id = p.id_profile 
    inner join m_profile mp on mp.id = prof.id_m_profile 
    where p.platform = 'facebook'
        and p.snapshot_date >= '{SNAPSHOT_DATE_FROM}'
        and p.snapshot_date <= '{SNAPSHOT_DATE_TO}'
    group by mp."name", p.snapshot_date, mp.url 
    order by COUNT(*) desc
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
	  prof.creation_date as "creación del perfil",
	  prof.followers as "seguidores" , prof."following" as "seguidos",
	  p.creation_date as "fecha post",
	  p.url as "url post", p.shares as "comparticiones",
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


if __name__ == '__main__':
    do_reports()
