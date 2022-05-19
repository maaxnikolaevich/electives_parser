from sqlalchemy import Table, Integer, String, Column, ForeignKey, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("past conn db url")
Base = declarative_base()


class BaseEntity:
    id = Column(Integer, primary_key=True)


tag_elective = Table(
    "tag_elective",
    Base.metadata,
    Column("elective_id", Integer(), ForeignKey("elective.id"), primary_key=True),
    Column("tag_id", Integer(), ForeignKey("tag.id"), primary_key=True),
)

author_elective = Table(
    "author_elective",
    Base.metadata,
    Column("elective_id", Integer(), ForeignKey("elective.id"), primary_key=True),
    Column("author_id", Integer(), ForeignKey("author.id"), primary_key=True),
)


class Elective(Base, BaseEntity):
    __tablename__ = "elective"
    title = Column(String(50), nullable=False)
    short_description = Column(String(50))
    full_description = Column(Text)
    minor_id = Column(Integer, ForeignKey("minor.id"), nullable=True)
    authors = relationship("Author", secondary=author_elective, backref="elective")
    tags = relationship("Tag", secondary=tag_elective, backref="elective")


class Minor(Base, BaseEntity):
    __tablename__ = "minor"
    title = Column(String(255), nullable=False)
    electives = relationship("Elective", backref="minor")


class Author(Base, BaseEntity):
    __tablename__ = "author"
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    electives = relationship("Elective", secondary=author_elective, backref="author")


class Tag(Base, BaseEntity):
    __tablename__ = "tag"
    name = Column(String(100), nullable=False)
    electives = relationship("Elective", secondary=tag_elective, backref="tag")
