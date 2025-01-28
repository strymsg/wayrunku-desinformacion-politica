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
class HashtagsPosts(DbBase):
    """Class to manage Hashtags and Posts relationship with the DB"""
    __tablename__ = 'hashtags_posts'
    
    id = Column(Integer, primary_key=True)
    id_hashtag = Column(Integer, ForeignKey('hashtags.id'), nullable=False)
    id_posts = Column(Integer, ForeignKey('posts.id'), nullable=False)
    
    snapshot_date = Column(Date, default=today_yyyymmdd())

