from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Article(Base):
    __tablename__ = 'Articles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    content = Column(String(), unique=True)
    comments = relationship('Comment')
    author_id = Column(Integer, ForeignKey('Users.id'))

    def __init__(self, name, content="", user_id=0):
        self.name = name
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return '<Article %r>' % self.id


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(64), unique=True)
    email = Column(String(), unique=True)

    def __init__(self, name, email, password):
        self.username = name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Comment(Base):
    __tablename__ = 'Comments'
    id = Column(Integer, primary_key=True)
    content = Column(String(1024), unique=False)
    article_id = Column(Integer, ForeignKey('Articles.id'))
    user_id = Column(Integer, ForeignKey('Users.id'))
    datetime = Column(DateTime())

    def __init__(self, datetime, content, user_id):
        self.datetime = datetime
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %r>' % self.id
