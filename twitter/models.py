"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):

    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")
    
    tweets = relationship("Tweet", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "@" + str(self.username)


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id

class Tweet(Base):
    # TODO: Complete the class
    __tablename__ = "tweets"

    id = Column("id", INTEGER, primary_key = True)
    content = Column("content", TEXT)
    timestamp = Column("timestamp", TEXT, nullable=False)
    username = Column("username", ForeignKey("users.username"))
    user = relationship("User", back_populates="tweets")
    tags = relationship("Tag", secondary="tweetTags", back_populates="tweets")

    def __init__(self, content, timestamp, username):
        self.content = content
        self.timestamp = timestamp
        self.username = username
    
    def __repr__(self):
        return str(self.user) + "\n" + str(self.content) + "\n" + str(self.tags) + "\n" + str(self.timestamp)

class Tag(Base):
    # TODO: Complete the class
    __tablename__ = "tags"

    id = Column("id", INTEGER, primary_key = True)
    content = Column("content", TEXT)
    tweets = relationship("Tweet",  secondary="tweetTags", back_populates="tags")
    
    def __init__(self, content):
        self.content = content
    
    def __repr__(self):

        return "#" + str(self.content)



class TweetTag(Base):
    # TODO: Complete the class
    __tablename__ = "tweetTags"

    id = Column("id", INTEGER, primary_key = True)
    tweet_id = Column("tweet_id", ForeignKey("tweets.id"))
    tag_id = Column("tag_id", ForeignKey("tags.id"))


    def __init__(self, tweet_id, tag_id):
        self.tweet_id = tweet_id
        self.tag_id = tag_id

