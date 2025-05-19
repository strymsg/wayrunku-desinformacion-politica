"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
from typing import Dict, List
#from sqlalchemy.orm import sessionmaker
from src.db.models.m_profile import MProfile as MProfileModel
from src.db.session import SessionHandler
from src.db.db_manager import DbBase, DbManager
from src.common.utils.custom_logger import CustomLogger
from src.common.utils.time import today_yyyymmdd

LOGGER = CustomLogger('m_profile DH ⛁')

db = DbManager.create()
engine = db.engine

class MProfileDatahandler():

    def __init__(self, session):
        """Initialize Data Handler
        Parameters:
        session (sqlalchemy sessionmaker instance): Session instance from sqlalchemy
        """
        self.sHandler = SessionHandler(session, MProfileModel)


    def insert(self, profile: Dict) -> Dict:
        LOGGER.debug(f'Inserting {profile}')
        try:
            self.sHandler.add({
                'name': profile['name'],
                'url': profile['url'],
                'creation_date': today_yyyymmdd()
            });
            self.sHandler.session.commit()
        except Exception as E:
            LOGGER.error(f'Error happened {E}')
            self.sHandler.session.rollback()
            raise E

        created = self.get_one_by(name=profile['name'])
        print(f"_____ CREATED: {created}")
        return created


    def get_one_by_name(self, name: str) -> Dict:
        LOGGER.debug(f'Get one by name {name}')
        existing = self.sHandler.get_one({ 'name': name })
        return existing
    

    def get_one_by(self, **fields) -> Dict:
        LOGGER.debug(f'Get one by {fields}')
        existing = self.sHandler.get_one(fields)
        return existing
