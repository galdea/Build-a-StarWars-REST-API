from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:///starwars.db', echo=True) 
db = SQLAlchemy()
Base = db.Model
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)

    def __repr__(self):
        return '<User {} {}>'.format(self.firstname, self.lastname)
    
    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

class Favorites(Base):
    __tablename__ = 'Favorites'
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('Characters.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('Planets.id'), primary_key=True)
    character = relationship("Character")
    planet = relationship("Planet")

    def __repr__(self):
        return '<Favorites {} {}>'.format(self.character.name, self.planet.name)
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "character": self.character.serialize(),
            "planet": self.planet.serialize()
        }

class Character(Base):
    __tablename__ = 'Characters'
    id = Column(Integer, primary_key=True)
    mass = Column(Integer)
    height = Column(Integer)
    hair_color = Column(String)
    skin_color = Column(String)
    eye_color = Column(String)
    birth_year = Column(String)
    species = Column(String)
    homeworld = Column(String)
    gender = Column(String)
    name = Column(String)

    def __repr__(self):
        return '<Character {}>'.format(self.name)
    
    def serialize(self):
        return {
            "id": self.id,
            "mass": self.mass,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "species": self.species,
            "homeworld": self.homeworld,
            "gender": self.gender,
            "name": self.name
        }

class Planet(Base):
    __tablename__ = 'Planets'
    id = Column(Integer, primary_key=True)
    diameter = Column(Integer)
    rotation_period = Column(Integer)
    orbital_period = Column(Integer)
    gravity = Column(String)
    population = Column(Integer)
    climate = Column(String)
    terrain = Column(String)
    surface_water = Column(Integer)
    name = Column(String)
    url = Column(String)

    def __repr__(self):
        return '<Planet {}>'.format(self.name)
    
    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "name": self.name,
            "url": self.url
        }

Base.metadata.create_all(engine)
