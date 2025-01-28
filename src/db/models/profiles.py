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
class Profiles(DbBase, BaseModelMembers):
    """Class to manage Profiles with the DB"""
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    id_m_profile = Column(Integer, ForeignKey('m_profile.id'), nullable=True)
    #TODO: id_profile_type (FK)

    snapshot_date = Column(Date, default=today_yyyymmdd())
    name = Column(String)
    creation_date = Column(Date)
    country_origin = Column(String)
    followers = Column(Integer)
    following = Column(Integer)
    platform = Column(String)
    url = Column(String)
    likes_got = Column(Integer)
    likes_in_posts_got = Column(Integer)
    posts = Column(Integer)
    comments = Column(Integer)
    mentions = Column(Integer)
    group_posts = Column(Integer)
    comments_got = Column(Integer)
    saves_got = Column(Integer)
    group_memberships = Column(Integer)
    video_plays = Column(Integer)
    lives = Column(Integer)
    short_videos = Column(Integer)
    react_like_got = Column(Integer)
    react_love_got = Column(Integer)
    react_haha_got = Column(Integer)
    react_sad_got = Column(Integer)
    react_wow_got = Column(Integer)
    react_angry_got = Column(Integer)
    hashtags = Column(Integer)
    hyperlinks = Column(Integer)        

    # dt.now().strftime('%Y-%m-%d') --> '2025-01-15'
    #TODO: constructor, Insert
