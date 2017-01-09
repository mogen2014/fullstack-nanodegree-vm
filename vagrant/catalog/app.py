from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import User, Genre, TVShow, Base

from flask import session as login_session
import string
import json
from flask import make_response
import requests
from login import mod
from database_setup import engine, session

import os
Base.metadata.bind = engine

app = Flask(__name__)
# register blueprint into this app
app.register_blueprint(mod)


@app.route('/')
def welcome():
    genres = session.query(Genre)
    # get the last ten actived items
    tvitems = session.query(TVShow).order_by(desc('created_time'))
    tvitems = tvitems.slice(0, 8)
    return render_template('show_tvitem_list.html',
                           login_session=login_session,
                           genres=genres,
                           selected_genre=None,
                           tvitems=tvitems)


@app.route('/<string:genre_name>')
def showOneGenre(genre_name):
    genres = session.query(Genre)
    genre_query = session.query(Genre).filter_by(name=genre_name)
    # check genre name is valid in database
    if genre_query.count() > 0:
        selected_genre = genre_query.one()
        genre_id = selected_genre.id
        tvitems = session.query(TVShow).filter_by(genre_id=genre_id)
        return render_template('show_tvitem_list.html',
                               tvitems=tvitems,
                               selected_genre=selected_genre,
                               genres=genres,
                               login_session=login_session)
    else:
        return make_response(json.dumps('Not Found.'), 404)


@app.route('/<string:genre_name>/create', methods=['GET', 'POST'])
def createTvitem(genre_name):
    genre_query = session.query(Genre).filter_by(name=genre_name)
    if request.method == 'GET':
        # check if GET request is valid
        if genre_query.count() > 0:
            current_genre = genre_query.one()
            return render_template('create_tvitem.html',
                                   tvitem=None,
                                   current_genre=current_genre,
                                   login_session=login_session)
        else:
            return make_response(json.dumps('Not Found.'), 404)
    if request.method == 'POST':
        tvitem_name = request.form['name']
        tvitem_description = request.form['description']
        genre_name = request.form['current_genre']

        current_genre = genre_query.one()
        img_url = request.form['img_url']
        user_id = getUserID(login_session['email'])
        # check if user input is empty
        if tvitem_name and tvitem_description:
            # tvitem_name.encode('utf-8').strip()
            # search if tvitem name already exists
            # if
            xx = session.query(TVShow).filter_by(name=tvitem_name).all()
            if xx:
                error_msg = '''The TVShow name you are trying
                to create has already been created.'''
                return render_template('create_tvitem.html',
                                       current_genre=current_genre,
                                       tvitem_name=tvitem_name,
                                       tvitem_description=tvitem_description,
                                       img_url=img_url,
                                       tvitem=None,
                                       error=error_msg,
                                       login_session=login_session)
            # if not exists, save it
            else:
                new_tvitemm = TVShow(name=tvitem_name,
                                     description=tvitem_description,
                                     genre_id=current_genre.id,
                                     img_url=img_url,
                                     user_id=user_id,)
                session.add(new_tvitemm)
                session.commit()
                url = '/' + current_genre.name
                flash('Created successfully.')
                return redirect(url)
        # either name or description is empty, give some
        # error message
        else:
            error_msg = 'Boath name and description can not be empty.'
            return render_template('create_tvitem.html',
                                   current_genre=current_genre,
                                   tvitem_name=tvitem_name,
                                   tvitem_description=tvitem_description,
                                   img_url=img_url,
                                   tvitem=None,
                                   error=error_msg,
                                   login_session=login_session)


@app.route('/<string:genre_name>/<string:tvitem_name>')
def showOneTvshow(genre_name, tvitem_name):
    genre_query = session.query(Genre).filter_by(name=genre_name)
    tvitem_query = session.query(TVShow).filter_by(name=tvitem_name)
    # check if genre name and tvitem name from
    # request URL is valid
    if tvitem_query.count() > 0 and genre_query.count() > 0:
        genre = genre_query.one()
        tvitem = tvitem_query.one()
        return render_template('show_one_tvitem.html',
                               tvitem=tvitem,
                               login_session=login_session)
    else:
        return make_response(json.dumps('Not Found.'), 404)


@app.route('/<string:genre_name>/<string:tvitem_name>/edit',
           methods=['GET', 'POST'])
def editTvitem(genre_name, tvitem_name):
    genre_query = session.query(Genre).filter_by(name=genre_name)
    tvitem_query = session.query(TVShow).filter_by(name=tvitem_name)
    if request.method == 'GET':
        # check if genre name and tvitem name from
        # request URL is valid
        if tvitem_query.count() > 0 and genre_query.count() > 0:
            tvitem = tvitem_query.one()
            return render_template('create_tvitem.html',
                                   tvitem=tvitem,
                                   login_session=login_session)
        else:
            return make_response(json.dumps('Not Found.'), 404)
    elif request.method == 'POST':
        tvitem = tvitem_query.one()
        tvitem_name = request.form['name']
        tvitem_description = request.form['description']
        genre_name = request.form['current_genre']

        genre_id = session.query(Genre).filter_by(name=genre_name).first().id

        img_url = request.form['img_url']
        # check if user input is empty
        if tvitem_name and tvitem_description:
            tvitem.name = tvitem_name
            tvitem.description = tvitem_description
            tvitem.img_url = img_url
            tvitem.genre_id = genre_id
            session.commit()
            url = '/' + genre_name
            flash('Saved successfully.')
            return redirect(url)
        # either name or description is empty
        # send some error message
        else:
            error_msg = 'Both name and description can not be empty.'
            return render_template('create_tvitem.html',
                                   current_genre=None,
                                   tvitem=tvitem,
                                   error=error_msg,
                                   login_session=login_session)


@app.route('/<string:genre_name>/<string:tvitem_name>/delete',
           methods=['GET', 'POST'])
def delteTvitem(genre_name, tvitem_name):
    genre = session.query(Genre).filter_by(name=genre_name).one()
    tvitem = session.query(TVShow).filter_by(
        genre=genre, name=tvitem_name).one()

    if request.method == 'GET':
        return render_template('delete_tvitem.html',
                               tvitem=tvitem,
                               login_session=login_session)
    elif request.method == 'POST':
        session.delete(tvitem)
        session.commit()
        flash('Deleted successfully.')
        url = '/' + genre_name
        return redirect(url)


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# api endpoints


@app.route('/json/<string:genre_name>/<string:tvitem_name>.json')
def getOneTvitemJSON(genre_name, tvitem_name):
    genre = session.query(Genre).filter_by(name=genre_name).one()
    tvitem = session.query(TVShow).filter_by(
        name=tvitem_name, genre_id=genre.id).one()
    # print (tvitem.serialize)
    return jsonify(tvitem=tvitem.serialize)


@app.route('/json/<string:genre_name>.json')
def getTvitemsJSON(genre_name):
    genre = session.query(Genre).filter_by(name=genre_name).one()
    items = session.query(TVShow).filter_by(genre_id=genre.id).all()
    response = jsonify(TV_Items=[x.serialize for x in items])
    return response


@app.route('/json/genres.json')
def getGenresJSON():
    genres = session.query(Genre).all()
    response = jsonify(Genres=[genre.serialize for genre in genres])
    # print response
    return response

app.secret_key = 'super secret key'
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'redis'

    app.debug = True
    # app.run(host='0.0.0.0', port=5000)

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
