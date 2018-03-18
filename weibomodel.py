import sqlite3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,BigInteger, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    """
    create table t_user(
        id INTEGER primary key AUTOINCREMENT,
        uid varchar(100) not null,
        token varchar(100) unique not null default '',
        expires int not null default 0,
        createtime TIMESTAMP default (datetime('now','localtime')),
        updatetime TIMESTAMP default '',
        state varchar(100) not null default '',
        code varchar(100)  not null default '',
        maxid bigint not null default 0
    )
    """
    __tablename__ = "t_user"
    id = Column(Integer, primary_key=True,autoincrement=True)
    uid = Column(String(100),default='')
    token = Column(String(100),unique=True,default='')
    expires = Column(Integer , default=0)
    createtime = Column(DateTime(), default=datetime.datetime.now())
    updatetime = Column(DateTime(), default=datetime.datetime.now() , onupdate=datetime.datetime.now())
    state = Column(String(100),default='')
    code = Column(String(100),default='')
    maxid = Column(BigInteger,default=0)


class HeavenMoive(Base):
    __tablename__ = "t_heavenmoive"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100),default='')
    pic_link = Column(String(100),default='')
    ftp = Column(String(100),default='')
    createtime = Column(DateTime(), default=datetime.datetime.now())
    updatetime = Column(DateTime(), default=datetime.datetime.now() , onupdate=datetime.datetime.now())
    doubanscore = Column(String(100),default='')
    imdbscore = Column(String(100),default='')
    content = Column(String(400),default='')
    movieurl = Column(String(100),unique=True,default='')

def droptable(engine):
    Base.metadata.drop_all(engine)

def createtable(engine):
    Base.metadata.create_all(engine)

def init_sqlalchemy(dbname='sqlite:///autoweibo.db'):
    DBSession = scoped_session(sessionmaker())
    engine = create_engine(dbname, echo=False)
    DBSession.remove()
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return engine , DBSession


def test_sqlalchemy_orm(engine , DBSession):
    user = User()
    user.uid = "xxx"
    user.token = "adfsafsf2"
    DBSession.add(user)
    DBSession.flush()
    DBSession.commit()


if __name__ == '__main__':
    engine , DBSession = init_sqlalchemy()
    droptable(engine)
    createtable(engine)
    test_sqlalchemy_orm(engine , DBSession)

