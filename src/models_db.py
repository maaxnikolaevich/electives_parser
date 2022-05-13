from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import relationship

engine = create_engine(
    'past conn db url'
)
Base = declarative_base()


class BaseEntity:
    id = Column(Integer, primary_key=True)


class Elective(Base, BaseEntity):
    __tablename__ = "elective"
    title = Column(String(50), nullable=False)
    short_description = Column(String(50), nullable=False)
    full_description = Column(String(255), nullable=False)
    minor = Column(Integer, ForeignKey('minor.id'))


class Minor(Base, BaseEntity):
    __tablename__ = "minor"
    title = Column(String(255), nullable=False)
    elective = relationship("Elective")


author_elective = Table('author_elective', Base.metadata,
                        Column('elective_id', Integer(), ForeignKey("elective.id")),
                        Column('author_id', Integer(), ForeignKey("author.id"))
                        )


class Author(Base, BaseEntity):
    __tablename__ = "author"
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)


tag_elective = Table('tag_elective', Base.metadata,
                     Column('elective_id', Integer(), ForeignKey("elective.id")),
                     Column('tag_id', Integer(), ForeignKey("tag.id"))
                     )


class Tag(Base, BaseEntity):
    __tablename__ = "tag"
    name = Column(String(100), nullable=False)
