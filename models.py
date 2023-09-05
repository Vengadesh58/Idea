from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Ideas(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, nullable=False)
    shortname = Column(String, nullable=False)
    define = Column(String, nullable=False)
    objective = Column(String, nullable=False)
    businessvalue = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    status = Column(String, nullable=False)
    createdby = Column(String, nullable=False)
    createdat = Column(TIMESTAMP(timezone=True),
                       nullable=False,   server_default=text('now()'))
    datasources = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    createdat = Column(TIMESTAMP(timezone=True),
                       nullable=False,   server_default=text('now()'))


class Comments(Base):
    __tablename__ = "comments"
    number = Column(Integer, primary_key=True, nullable=False)
    id = Column(Integer, ForeignKey(
        "ideas.id", ondelete="CASCADE"), nullable=False)
    comments = Column(String, nullable=True)
    createdby = Column(String, nullable=False)
    createdat = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text('now()'))