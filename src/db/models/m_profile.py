"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import insert, select, update, func
from sqlalchemy import text
from src.db.db_manager import DbManager, DbBase
from src.db.models.base_model_memebers import BaseModelMembers
from src.common.utils.time import today_yyyymmdd


@dataclass
class MProfile(DbBase, BaseModelMembers):
    """Class to manage Monitored Profile with the DB"""
    __tablename__ = 'm_profile'
    __tableargs__ = (UniqueConstraint('id', 'name'))

    
    id = Column(Integer, primary_key=True)
    #TODO: id_profile_type (FK)

    name = Column(String, unique=True)
    url = Column(String)
    creation_date = Column(Date, default=today_yyyymmdd())

    # def row2dict(row):
    #     d = {}
    #     for column in row.__table__.columns:
    #         d[column.name] = str(getattr(row, column.name))
        
    #     return d
