"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""
from typing import Dict, List

from src.db.models.posts import Posts as PostsModel
from src.db.session import SessionHandler
from src.facebook.data_handlers.profiles import ProfilesDatahandler
from src.db.db_manager import DbBase, DbManager
from src.common.utils.custom_logger import CustomLogger
from src.common.utils.time import today_yyyymmdd, age_in_days, datetime_from_yyyymmdd
from src.common.utils.parsers import get_number_facebook, facebook_date_text_parser


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
        react_like_got = 0
        react_love_got = 0
        react_haha_got = 0
        react_sad_got = 0
        react_wow_got = 0
        react_wow_got = 0
        react_angry_got = 0
        react_icare_got = 0
        comments_in_posts_got = 0
        print('::::::::')
        print(profile_data)

        registered_posts = []
        for i, post in enumerate(profile_data['posts']):
            print('>>>', post)
            LOGGER.debug(f"Checking post ({i}/{len(profile_data['posts'])})")
            post['creation_date'] = post['creation_date']
            
            post_age = age_in_days(datetime_from_yyyymmdd(post['creation_date']))
            if post_age > max_days_age is False:
                LOGGER.debug(f'Post date {post["creation_date"]} is too old (max age: {max_days_age} skipping.')
                continue

            to_register = {
                'id_profile': profile_data['id'],
                'snapshot_date': today_yyyymmdd(),
                'creation_date': post['creation_date'],
                'url': post['url'],
                'content': post['content'],
                'media_content': post['media_content'],
                'platform': 'facebook',
                'post_type': post['post_type'],
                # TODO: register hashtags
                # 'hashtags': ','.join(post['tags']),
                'likes_got': int(post['react_like_got']) if post['react_like_got'] != '' else 0,
                'comments_got': int(post['comments_got']) if post['comments_got'] != ''  else 0,
                'shares': int(post['shares']) if post['shares'] != '' else 0,
                'react_like_got': int(post['react_like_got']) if post['react_like_got'] != '' else 0,
                'react_love_got': int(post['react_love_got']) if post['react_love_got'] != '' else 0,
                'react_haha_got': int(post['react_haha_got']) if post['react_haha_got'] != '' else 0,
                'react_sad_got': int(post['react_sad_got']) if post['react_sad_got'] != '' else 0,
                'react_wow_got': int(post['react_wow_got']) if post['react_wow_got'] != '' else 0,
                'react_angry_got': int(post['react_angry_got']) if post['react_angry_got'] != '' else 0,
                'react_icare_got': int(post['react_icare_got']) if post['react_icare_got'] != '' else 0,
                'total_reactions': int(post['total_reactions']),
                'is_shared': post['is_shared'] if post['is_shared'] != 0 else 0,
                'extraction_status': 'completed',
                # TODO:
                #'is_shared':
                # hyperlinks
            }
            try:
                registered = self.upsert_for_today(to_register)
                registered_posts.append(registered)
            except Exception as e:
                LOGGER.error(f'Error upserting post: {LOGGER.format_exception(e)}')

            likes_in_posts_got += to_register['react_like_got']
            react_like_got += to_register['react_like_got']
            react_love_got += to_register['react_love_got']
            react_haha_got += to_register['react_haha_got']
            react_sad_got += to_register['react_sad_got']
            react_wow_got += to_register['react_wow_got']
            react_angry_got += to_register['react_angry_got']
            react_icare_got += to_register['react_icare_got']
            comments_in_posts_got += to_register['comments_got']

        try:
            profile_updated = self.profiles_dh.upsert_for_today({
                'id': profile_data['id'],
                'name': profile_data['name'],
                'likes_in_posts_got': likes_in_posts_got,
                'react_like_got': react_like_got,
                'react_love_got': react_love_got,
                'react_haha_got': react_haha_got,
                'react_sad_got': react_sad_got,
                'react_wow_got': react_wow_got,
                'react_angry_got': react_angry_got,
                'react_icare_got': react_icare_got,
                'comments_got': comments_in_posts_got
            })
        except Exception as e:
            LOGGER.error(f'Error updating profile {profile_data} likes and comments')
            LOGGER.error(LOGGER.format_exception(e))
            
        return registered_posts
