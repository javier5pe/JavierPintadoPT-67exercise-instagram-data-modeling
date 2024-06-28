import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person')
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    followers = relationship('Followers', 
                             primaryjoin="User.id==Followers.user_from_id",
                             back_populates="user_from")
    following = relationship('Followers',
                             primaryjoin="User.id==Followers.user_to_id",
                             back_populates="user_to")

class Followers(Base):
    __tablename__ = 'followers'
    user_from_id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
    user_to_id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="followers")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="following")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    post = relationship("Post", back_populates="media")

def to_dict(self):
    return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
