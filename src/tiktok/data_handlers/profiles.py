"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
from typing import Dict, List

from src.db.models.profiles import Profiles as ProfilesModel
from src.db.session import SessionHandler
from src.db.db_manager import DbBase, DbManager
from src.common.utils.custom_logger import CustomLogger
from src.common.utils.time import today_yyyymmdd
from src.tiktok.data_handlers.m_profile import MProfileDatahandler


LOGGER = CustomLogger('profiles DH ⛁:')


db = DbManager.create()
engine = db.engine
# Session = sessionmaker(bind=engine)
# session = Session()

class ProfilesDatahandler():
    
    def __init__(self, session):
        """Initialize Data Handler
        Parameters:
        session (sqlalchemy sessionmaker instance): Session instance from sqlalchemy
        """
        self.sHandler = SessionHandler(session, ProfilesModel)
        self.mProfile_dh = MProfileDatahandler(session)
        #self.profiles_session = SessionHandler(session, ProfilesModel)
        #self.mProfile_dh = mProfileDatahandler()


    def insert(self, profile_data: dict) -> Dict:
        """Inserts a profile snapshot record and returns the result created. Automatically
        does the relationship between this and monitored profile.
        """
        LOGGER.debug(f'Inserting {profile_data}')
        m_profile = self.mProfile_dh.get_one_by(name=profile_data['name'])
        if m_profile is None:
            self.mProfile_dh.insert({
                'name': profile_data['name'],
                'url': profile_data['url'],
            })
            m_profile = self.mProfile_dh.get_one_by(name=profile_data['name'])
        
        to_add = {**profile_data, **{'id_m_profile': m_profile['id']}}
        try:
            self.sHandler.add(to_add)
            self.sHandler.session.commit()
        except Exception as E:
            LOGGER.error(f'Error while inserting: {E}')
            self.sHandler.session.rollback()
            raise E

        profile = self.sHandler.get_one({
            'name': to_add['name'],
            'id_m_profile': to_add['id_m_profile']
        })
        print(f" profile added: {profile}")
        return profile


    def update(self, profile_data: dict) -> Dict:
        """Updates the given profile data. Assumes id is passed

        Parameters:
        profile_data: Profile data dictionary, assumes to have fields id, name
        """
        LOGGER.debug(f'Updating {profile_data["name"], profile_data["snapshot_date"]}')
        profile = self.get_one_by(id=profile_data['id'])
        if profile is None:
            LOGGER.warn(f'No profile found with id: {profile_data["id"]}')
            return {}

        try:
            self.sHandler.update({
                'id': profile_data['id'],
                'name': profile_data['name'],
            }, profile_data)
            self.sHandler.session.commit()
            return self.get_one_by(id=profile_data['id'])
        except Exception as E:
            LOGGER.error(f'Error while updating: {E}')
            self.sHandler.session.rollback()
            raise E
        

    def upsert_for_today(self, profile_data: Dict) -> Dict:
        """Inserts or updates a profile, if it exists and the last record
        has a different snapshot date creates a new one, otherwise updates
        the record with the same snapshot_date as today.

        Parameters:
        profile_data: Profile Data

        Returns
        profile updated or created
        """
        LOGGER.debug(f'Upsert for today {profile_data["name"]} {today_yyyymmdd()}')
        profile = self.get_one_by(name=profile_data['name'])
        if profile is None:
            LOGGER.warn(f'No profile found with id: {profile_data["name"]}')
            return self.insert(profile_data)
        
        profile = self.get_one_by(
            name=profile_data['name'],
            snapshot_date=today_yyyymmdd()
        )
        if profile is not None:
            LOGGER.debug(f'Updating profile last with snapshot_date = {today_yyyymmdd()}')
            to_update = {**profile_data, **{
                'id_m_profile': profile['id_m_profile'],
                'id': profile['id'],
                'snapshot_date': profile['snapshot_date']
            }}
            return self.update(to_update)
        return self.insert(profile_data)


    def get_one_by(self, **fields) -> Dict:
        LOGGER.debug(f'Get one by {fields}')
        existing = self.sHandler.get_one(fields)
        return existing

