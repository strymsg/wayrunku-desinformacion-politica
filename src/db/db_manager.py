"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.common.utils.custom_logger import CustomLogger

DbBase = declarative_base()


LOGGER = CustomLogger('DB Manager ⛁: ')


class DbManager:
    """
    Extracted from https://gist.github.com/emmanuelnk/db62507184125ddfe24844bb552fc26d
    """
    __instance = None


    def __init__(self):
        """ Virtually private constructor. """
        LOGGER.debug("Initialize ")
        if DbManager.__instance is not None:
            raise Exception("This class is a singleton, use DbManager.create()")
        else:
            DbManager.__instance = self
        self.engine = self.create_engine()


    @staticmethod
    def create():
        if DbManager.__instance is None:
            DbManager.__instance = DbManager()

        return DbManager.__instance

    def create_engine(self):
        #DATABASE_URL = "postgresql://postgres:postgres@localhost/socialmedia1"
        LOGGER.info("Create Engine")
        #credentials = DB.get_credentials()

        # return sqlalchemy.create_engine('{engine}://{user}:{password}@{host}:{port}/{database}'.format(
        #     engine='postgres+psycopg2',
        #     user=credentials['username'],
        #     password=credentials['password'],
        #     host=credentials['host'],
        #     port=int(credentials['port']),
        #     database=credentials['database']
        # ),
        #     pool_size=200,
        #     max_overflow=0,
        #     echo=bool(os.getenv('POSTGRESQL_DEBUG', False))
        # )
        #return create_engine(DATABASE_URL, pool_size=200, echo=False)

        return create_engine('{engine}://{user}:{password}@{host}:{port}/{database}'.format(
            #engine='postgres+psycopg2',
            engine='postgresql+psycopg2',
            user='postgres',
            password='postgres',
            host='localhost',
            port=int('5432'),
            database='socialmedia1'
        ),
            pool_size=200,
            max_overflow=0,
            #echo=True
            echo=False
        )


    def connect(self):
        LOGGER.info("Connect engine")
        return self.engine.connect()

