import pandas as pd
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///amet.db", echo=True)


class PaintingsData(Base):
    __tablename__ = "paintingsData"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    tech = Column("tech", String)
    size = Column("size", String)
    price = Column("price", Integer)
    img = Column("img", String)
    created = Column("created", String)
    soldDate = Column("soldDate", String)
    sold = Column("sold", BOOLEAN)
    reserved = Column("reserved", BOOLEAN)
    reservedDate = Column("reservedDate", String)
    showDOM = Column("showDOM", BOOLEAN)
    registerNum = Column("registerNum", Integer)

    def __init__(self, id, title, tech, size, price, img, created, soldDate, sold, reserved, reservedDate, showDOM, registerNum):
        self.id = id
        self.title = title
        self.tech = tech
        self.size = size
        self.price = price
        self.img = img
        self.created = created
        self.soldDate = soldDate
        self.sold = sold
        self.reserved = reserved
        self.reservedDate = reservedDate
        self.showDOM = showDOM
        self.registerNum = registerNum

    def __repr__(self):
        return f"({self.id}) {self.title} {self.tech} {self.size} ({self.price}) {self.img} ({self.created}) {self.soldDate} {self.sold}) {self.reserved} {self.reservedDate} {self.showDOM} ({self.registerNum})"


class Customer(Base):
    __tablename__ = "customers"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    last_name = Column("last_name", String)
    email = Column("email", String)
    telephone = Column("telephone", Integer)
    country = Column("country", String)
    feedback = Column("feedback", String)
    registerNum = Column(Integer, ForeignKey("paintingsData.registerNum"))

    def __init__(self, id, name, last_name, email, telephone, country, feedback, registerNum):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.country = country
        self.feedback = feedback
        self.registerNum = registerNum

    def __repr__(self):
        return f"{self.id} {self.name} {self.last_name} {self.email} {self.telephone} {self.country} {self.feedback} ({self.registerNum})"


class Fan(Base):
    __tablename__ = "fans"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    last_name = Column("last_name", String)
    email = Column("email", String)
    telephone = Column("telephone", Integer)
    country = Column("country", String)
    feedback = Column("feedback", String)

    def __init__(self, id, name, last_name, telephone, country, email, feedback):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.country = country
        self.feedback = feedback

    def __repr__(self):
        return f"{self.id} {self.name} {self.last_name} {self.email} {self.telephone} {self.country} {self.feedback}"


engine = create_engine("sqlite:///amet.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
