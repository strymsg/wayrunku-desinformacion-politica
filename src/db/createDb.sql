-- drop table m_profile, profiles, posts, hashtags, hashtags_posts CASCADE

CREATE TABLE m_profile(
       id SERIAL PRIMARY KEY,
       name TEXT,
       url TEXT,
       creation_date DATE,
       UNIQUE(name)
);

CREATE TABLE profiles(
       id SERIAL PRIMARY KEY,
       id_m_profile INT NOT NULL,
       -- TODO: profile type FK
       snapshot_date DATE,

       name TEXT,
       creation_date DATE,
       country_origin TEXT,
       followers INT,
       following INT,
       platform TEXT,
       url TEXT,
       likes_got INT,
       posts INT,
       comments INT,
       mentions INT,
       group_posts INT,
       comments_got INT,
       saves_got INT,
       group_memberships INT,
       video_plays INT,
       lives INT,
       short_videos INT,
       react_love_got INT,
       react_haha_got INT,
       react_sad_got INT,
       react_wow_got INT,
       react_angry_got INT,
       react_like_got INT,
       hashtags INT,
       hyperlinks INT,

       FOREIGN KEY(id_m_profile) REFERENCES m_profile(id)
);
CREATE TABLE posts(
       id SERIAL PRIMARY KEY,
       id_profile INT NOT NULL,

       snapshot_date DATE,
       creation_date DATE,
       url TEXT,
       content TEXT,
       platform TEXT,
       is_shared INT,
       shares INT,
       likes_got INT,
       post_type TEXT,
       saves_got INT,
       react_love_got INT,
       react_haha_got INT,
       react_sad_got INT,
       react_wow_got INT,
       react_angry_got INT,
       react_like_got INT,
       hashtags INT,
       hyperlinks INT,

       FOREIGN KEY (id_profile)  REFERENCES profiles(id)
);

CREATE TABLE hashtags (
      id SERIAL PRIMARY KEY,
      name TEXT,
      followers INT
);

CREATE TABLE hashtags_posts(
       id SERIAL PRIMARY KEY,
       id_hashtag INT,
       id_post INT,
       snapshot_date DATE,
       name TEXT,
       FOREIGN KEY(id_hashtag) REFERENCES hashtags(id),
       FOREIGN KEY(id_post) REFERENCES posts(id)
);

-- select * from m_profile mp 
