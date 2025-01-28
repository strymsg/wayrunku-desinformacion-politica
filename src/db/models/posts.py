"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
import logging
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import insert, select, update, func
from sqlalchemy import text
from src.common.db_manager import db_engine, DbBase
from src.common.utils.time import today_yyyymmdd


@dataclass
class Posts(DbBase):
    """Class to manage Posts with the DB"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    id_profile = Column(Integer, ForeignKey('profiles.id'))
    id_source_post = Column(Integer, ForeignKey('posts.id'), nullable=True)

    snapshot_date = Column(Date, default=today_yyyymmdd())
    creation_date = Column(Date)
    content = Column(String)
    platform = Column(Integer)
    is_shared = Column(Integer, default=0)
    shares = Column(Integer)
    post_type = Column(String, default='post')
    
    react_like_got = Column(Integer)
    react_love_got = Column(Integer)
    react_haha_got = Column(Integer)
    react_sad_got = Column(Integer)
    react_wow_got = Column(Integer)
    react_angry_got = Column(Integer)
    hashtags = Column(Integer)
    hyperlinks = Column(Integer)
