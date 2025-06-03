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
from src.db.db_manager import DbBase
from src.db.models.base_model_memebers import BaseModelMembers
from src.common.utils.time import today_yyyymmdd


@dataclass
class Posts(DbBase, BaseModelMembers):
    """Class to manage Posts with the DB"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    id_profile = Column(Integer, ForeignKey('profiles.id'))
    id_source_post = Column(Integer, ForeignKey('posts.id'), nullable=True)

    snapshot_date = Column(Date, default=today_yyyymmdd())
    creation_date = Column(Date)
    url = Column(String)
    content = Column(String)
    media_content = Column(String)
    platform = Column(Integer)
    is_shared = Column(Integer, default=0)
    shares = Column(Integer)
    views = Column(Integer)
    likes_got = Column(Integer)
    comments_got = Column(Integer)
    post_type = Column(String, default='post')
    
    react_like_got = Column(Integer)
    react_love_got = Column(Integer)
    react_haha_got = Column(Integer)
    react_sad_got = Column(Integer)
    react_wow_got = Column(Integer)
    react_angry_got = Column(Integer)
    react_icare_got = Column(Integer)
    total_reactions = Column(Integer)
    hashtags = Column(Integer)
    hyperlinks = Column(Integer)
    extraction_status = Column(String, default='incomplete')
