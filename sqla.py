# -*- coding: utf-8 -*-
"""Sqlalchemy initialization"""
import os

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker

PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PATH, 'db')

os.system('which vmtouch && vmtouch -t {} >> debug.log'.format(DB_PATH))

# automap base
Base = automap_base()

# engines
api_eng = create_engine('sqlite:///{}'.format(os.path.join(DB_PATH, 'api.sqlite3')))
pro_eng = create_engine('sqlite:///{}'.format(os.path.join(DB_PATH, 'products.sqlite3')))

# reflect
Base.prepare(pro_eng, reflect=True)

P1 = Base.classes.p1
P2 = Base.classes.p2

P1_COL = inspect(P1).columns.keys()
P2_COL = inspect(P2).columns.keys()

Base.prepare(api_eng, reflect=True)

Api1 = Base.classes.api1
Api2 = Base.classes.api2
Api3 = Base.classes.api3

API3_COL = inspect(Api3).columns.keys()

# sessions
Session = scoped_session(sessionmaker(bind=pro_eng))
API_Session = scoped_session(sessionmaker(bind=api_eng))
# session = Session()


# close functions for django views
def close_sqla(sender, **kwargs):
    Session.close()


def close_api(*args):
    API_Session.close()
