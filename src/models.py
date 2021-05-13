from flask_login import UserMixin
from . import db
from .init_db import setup_db, create_table, get_engine
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

from datetime import datetime


# create model for user and add usermixin attributes to let flask-login work with it
class Users(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user = db.Column(db.String(145), unique=True)
    password = db.Column(db.String(145))

# setup users create table
def Users_Setup():
    meta = setup_db()
    # create the table
    users = Table(
        'users', meta,
        Column('id', Integer, primary_key=True),
        Column('user', String(100), nullable=False),
        Column('password', String(100), nullable=False),
        sqlite_autoincrement=True
    )
    # link to and create table
    engine = get_engine()
    meta.create_all(engine)
    return users

# nests table
def Nests():
    meta = setup_db()
    # create table for database
    nests = Table(
            'Nests', meta,
            Column('id', Integer, primary_key=True),
            Column('name', String(100), nullable=False),
            sqlite_autoincrement=True
    )
    # connect to database
    engine = get_engine()
    meta.create_all(engine)

    return nests
# species table
def Species():
    meta = setup_db()

    # species table
    species = Table(
        'Species', meta,
        Column('id', Integer, primary_key=True),
        Column('species', String(100), nullable=False),
        sqlite_autoincrement=True

    )
    # create connection
    engine = get_engine()
    meta.create_all(engine)
    return species

# create the big observations table
def Observations():
    meta = setup_db()

    # create table
    observations = Table(
        'Observations', meta,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, nullable=False),
        Column('nest_id', Integer, nullable=False),
        Column('species_id', Integer, nullable=False),
        Column('date', db.DateTime, nullable=False),
        Column('comment', String(500), nullable=False),
        Column('num_eggs', Integer, nullable=False),
        Column('live_young', Integer, nullable=False),
        Column('dead_young', Integer, nullable=False),
        Column('nest_flagged', db.Boolean, nullable=False),
        Column('cow_present', db.Boolean, nullable=False),
        sqlite_autoincrement=True
    )
    # connect to database and create
    engine = get_engine()
    meta.create_all(engine)
    return observations
