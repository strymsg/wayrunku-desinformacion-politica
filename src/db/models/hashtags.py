"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import insert, select, update, func
from sqlalchemy import text
from src.common.db_manager import db_engine, DbBase


@dataclass
class Hashtags(DbBase):
    """Class to manage Hashtags with the DB"""
    __tablename__ = 'hashtags'
    
    id = Column(Integer, primary_key=True)

    snapshot_date = Column(Date, default=today_yyyymmdd())
    name = Column(String)

