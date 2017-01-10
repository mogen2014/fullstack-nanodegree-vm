This is an simple web app which you can login with your social account, add your favorate TV Shows on it.
Try it directly [here on heroku](http://jojojojojojoe.herokuapp.com/),
or you can download this project from [Github](https://github.com/mogen2014/fullstack-nanodegree-vm/tree/master/vagrant/catalog)

## Dependency

To run this program you need to have the [python](https://www.python.org/downloads/) environment, I'm using python2 and it works well, but I have not tested it in python3 environment yet :)

### Web page

Some web related lib is used to make the web page looks nicer and  easily created, all of them are included in html header, so you need to make sure your network is good to get those resource. They are:

- [bootstrap](http://getbootstrap.com)
- [jQuery](jquery.com)

### Server side

- [Flask](https://flask.pocoo.org) is used to handle almost all web requests and response.
- [sqlalchemy](https://sqlalchemy-utils.readthedocs.io) is used as ORM to handle database CRUD actions, it's a great tool to talk to your database. What should be noticed is that I set enging to `engine = create_engine('postgresql://catalog:1234@localhost/tv')`, this postgresql's role name and password should be matched to your environment.
- [postgresql](https://postgresql.org) is the database to store data on server. 
- [oauth2client](https://oauth2client.readthedocs.io) is the library used as authentication and authorization.

## How To

- First make sure you habe installed all the library that this project depend on, then clone it from [Github](https://github.com/mogen2014/fullstack-nanodegree-vm/tree/master/vagrant/catalog)
- Go to your terminal 'cd' into this project's directory `python app.py`, if there are not some error messages, you can test it on your browser just open `http://localhost:5000`
