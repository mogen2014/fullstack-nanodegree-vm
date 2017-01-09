import os
import sys
import urlparse
from sqlalchemy import Column, ForeignKey, Integer, String, func, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine
from flask import Flask

Base = declarative_base()

# here is important part to avoid Thread Error like
# "(ProgrammingError) SQLite objects created in a thread can
# only be used in that same thread.", use scoped_session ,
# other module import from here, make sure engine object
# add connect_args={'check_same_thread': False}
# I saw people in stackoverflow.com said that
# session and db should only created once per thread,
# engine = create_engine('sqlite:////home/vagrant/tvshows.db',connect_args={'check_same_thread': False})

# I chose sqlite as database at previous version
# engine = create_engine('sqlite:///{}'.format('/home/vagrant/db/tvshows.db'),connect_args={'check_same_thread': False})

# heroku deploy on sqlite...
# engine = create_engine('sqlite:///tv.db')

engine = create_engine('postgresql://catalog:1234@localhost/tv')


DBSession = sessionmaker(bind=engine)
Session = scoped_session(DBSession)
session = Session()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String)


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    created_time = Column(TIMESTAMP, server_default=func.now(),
                          onupdate=func.current_timestamp())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_time': self.created_time
        }


class TVShow(Base):
    __tablename__ = 'tvshows'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String)
    img_url = Column(String)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship(Genre)
    created_time = Column(TIMESTAMP, server_default=func.now(),
                          onupdate=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'img_url': self.img_url,
            'genre': self.genre.name,
            'created_time': self.created_time
        }


# drop all table before created if schemes are changed
# or something, for testing
# Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
