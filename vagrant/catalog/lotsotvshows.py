from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, TVShow, User, Base, engine

import json

# engine = create_engine('sqlite:///tvshows.db')
# reset the database before insert some data
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


user = User(name='Joe', email='xiaojun0lee@gmail.com')
session.add(user)
session.commit()

dramas = json.loads(open('Drama.json').read())['TV_Items']
crimes = json.loads(open('Crime.json').read())['TV_Items']


genre_names = ['Drama', 'Comedy', 'Family', 'Crime']
for genre_name in genre_names:
    genre = Genre(name=genre_name)
    user_id = user.id
    session.add(genre)
    session.commit()

for drama in dramas:
    d = TVShow(name=drama['name'],
                description=drama['description'],
                genre_id=1,
                user_id=user.id,
                img_url=drama['img_url'])
    session.add(d)
    session.commit()
for crime in crimes:
    c = TVShow(name=crime['name'],
                description=crime['description'],
                genre_id=4,
                user_id=user.id,
                img_url=crime['img_url'])
    session.add(c)
    session.commit()
