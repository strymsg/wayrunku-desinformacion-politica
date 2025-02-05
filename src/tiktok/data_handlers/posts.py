"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
from typing import Dict, List

from src.db.models.posts import Posts as PostsModel
from src.db.session import SessionHandler
from src.tiktok.data_handlers.profiles import ProfilesDatahandler
from src.db.db_manager import DbBase, DbManager
from src.common.utils.custom_logger import CustomLogger
from src.common.utils.time import today_yyyymmdd, age_in_days, datetime_from_yyyymmdd
from src.common.utils.parsers import tiktok_date_parser, get_number_tiktok



LOGGER = CustomLogger('posts DH  ⛁:')

db = DbManager.create()
engine = db.engine


class PostsDataHandler():

    def __init__(self, session):
        """Initialize Data Handler
        Parameters:
        session (sqlalchemy sessionmaker instance): Session instance from sqlalchemy
        """
        self.sHandler = SessionHandler(session, PostsModel)
        self.profiles_dh = ProfilesDatahandler(session)

    def insert(self, post_data: Dict) -> Dict:
        """Inserts a posts snapshot record and returns the result created.
        Also creates the relationship between this and profile
        """
        LOGGER.debug(f'Inserting {post_data}')
        try:
            self.sHandler.add(post_data)
            self.sHandler.session.commit()
        except Exception as E:
            LOGGER.error(f'Error while inserting: {LOGGER.format_exception(E)}')
            self.sHandler.session.rollback()
            raise E
        post_data = self.sHandler.get_one({
            'url': post_data['url'],
        })
        return post_data


    def update(self, post_data: dict) -> Dict:
        """Updates the given post data. Assumes id is passed

        Parameters:
        post_data: Post data dictionary, assumes to have fields id, url
        """
        LOGGER.debug(f'Updating {post_data["url"], post_data["snapshot_date"]}')
        profile = self.get_one_by(id=post_data['id'])
        if profile is None:
            LOGGER.warn(f'No post found with id: {post_data["id"]}')
            return None

        try:
            self.sHandler.update({
                'id': post_data['id'],
                'url': post_data['url'],
            }, post_data)
            self.sHandler.session.commit()
            return self.get_one_by(id=post_data['id'])
        except Exception as E:
            LOGGER.error(f'Error while updating: {LOGGER.format_exception(E)}')
            self.sHandler.session.rollback()
            raise E


    def upsert_for_today(self, post_data: Dict) -> Dict:
        """Inserts or updates a post, if it exists and the last record
        has a different snapshot date creates a new one, otherwise updates
        the record with the same snapshot_date as today.

        Parameters:
        post_data: Post Data

        Returns
        post updated or created
        """
        LOGGER.debug(f'Upsert for today {post_data["url"]} {today_yyyymmdd()}')
        post = self.get_one_by(url=post_data['url'])
        if post is None:
            LOGGER.warn(f'No post found with url: {post_data["url"]}')
            return self.insert(post_data)
        
        post = self.get_one_by(
            url=post_data['url'],
            snapshot_date=today_yyyymmdd()
        )
        if post is not None:
            LOGGER.debug(f'Updating post last with snapshot_date = {today_yyyymmdd()}')
            to_update = {**post_data, **{
                'id': post['id'],
                'id_profile': post['id_profile'],
                'snapshot_date': post['snapshot_date']
            }}
            return self.update(to_update)
        return self.insert(post_data)

        
    def get_one_by(self, **fields) -> Dict:
        LOGGER.debug(f'Get one by {fields}')
        existing = self.sHandler.get_one(fields)
        return existing


    def register_all_posts_from_profile(
            self,
            profile_data: Dict,
            max_days_age: int) -> List[Dict]:
        """Register all posts from profile data dictionary. It also calculates
        total number of likes got in posts and total number of comments, saves
        this last two in the respective profile.
        
        Parameters:
        profile_data (Dict): Profile Data dictionary that includes videos list
        max_days_age (int): Max age in days that it is allowed to save a post.

        Returns: List of registered posts
        """
        likes_in_posts_got = 0
        comments_in_posts_got = 0

        registered_posts = []
        for i, video in enumerate(profile_data['videos']):
            LOGGER.debug(f"Checking video ({i/len(profile_data['videos'])})")
            video['date'] = tiktok_date_parser(video['date'])
            
            video_age = age_in_days(
                datetime_from_yyyymmdd(
                    tiktok_date_parser(video['date'])
                ))
            if video_age > max_days_age and video['pinned'] is False:
                LOGGER.debug(f'Video date {video["date"]} is too old (max age: {max_days_age} skipping.')
                continue

            to_register = {
                'id_profile': profile_data['id'],
                'snapshot_date': today_yyyymmdd(),
                'creation_date': video['date'],
                'url': video['url'],
                'content': video['description'],
                'platform': 'tiktok',
                # TODO: register hashtags
                'hashtags': ','.join(video['tags']),
                'likes_got': get_number_tiktok(video['likes']),
                'comments_got': get_number_tiktok(video['commentCount']),
                'extraction_status': 'completed',
                'views': get_number_tiktok(video['views']),
                # TODO:
                #'is_shared':
                #'post_type'
                #'shares'
                #
            }
            try:
                registered = self.upsert_for_today(to_register)
                registered_posts.append(registered)
            except Exception as e:
                LOGGER.error(f'Error upserting post: {LOGGER.format_exception(e)}')

            likes_in_posts_got += int(get_number_tiktok(video['likes']))
            comments_in_posts_got += int(get_number_tiktok(video['commentCount']))
            

        try:
            profile_updated = self.profiles_dh.upsert_for_today({
                'id': profile_data['id'],
                'name': profile_data['name'],
                'likes_in_posts_got': likes_in_posts_got,
                'comments_got': comments_in_posts_got
            })
        except Exception as e:
            LOGGER.error(f'Error updating profile {profile_data} likes and comments')
            LOGGER.error(LOGGER.format_exception(e))
            
        return registered_posts
