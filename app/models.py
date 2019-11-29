from sqlalchemy import Column, Integer, String
from app.database import Base

class Article(Base):
    __tablename__ = 'Articles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    content = Column(String(), unique=True)

    def __init__(self, name=None, content=""):
        self.name = name
        self.content = content

    def __repr__(self):
        return '<User %r>' % (self.name)