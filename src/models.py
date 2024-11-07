import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import declarative_base, relationship
from eralchemy import render_er

Base = declarative_base()

# Clase Planet (Planeta)
class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    population = Column(Integer)
    gravity = Column(String(40))
    climate = Column(String(50))
    terrain = Column(String(50))
    created = Column(String(50))
    surface_water = Column(Integer)
    diameter = Column(Integer)
    orbital_period = Column(Integer)
    rotation_period = Column(Integer)
    pic = Column(String(500))
    url = Column(String(100))

    # Relación con Persona y Favorites
    persons = relationship("Persona", backref="homeworld_relation", lazy=True)
    favorites = relationship("Favorites", backref="planet_favorites", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "created": self.created,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "pic": self.pic,
            "url": self.url
        }

# Clase Species (Especies)
class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    classification = Column(String(50))
    designation = Column(String(50))
    average_height = Column(Integer)
    skin_colors = Column(String(100))
    hair_colors = Column(String(100))
    eye_colors = Column(String(100))
    homeworld_id = Column(Integer, ForeignKey('planet.id'))  # Relación con Planet

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "skin_colors": self.skin_colors,
            "hair_colors": self.hair_colors,
            "eye_colors": self.eye_colors,
            "homeworld": self.homeworld_id
        }

# Clase Persona (Personaje)
class Persona(Base):
    __tablename__ = 'persona'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    birth_year = Column(Date, nullable=False)
    created = Column(String(50))
    homeworld_id = Column(Integer, ForeignKey('planet.id'))  # Relación con Planet
    eye_color = Column(String(10))
    gender = Column(String(15))
    hair_color = Column(String(20))
    height = Column(Integer)
    mass = Column(Integer)
    skin_color = Column(String(20))
    pic = Column(String(500))
    url = Column(String(100))

    # Relación con Favorites
    favorites = relationship("Favorites", backref="persona_favorites", lazy=True)

    # Relación con Species
    species_id = Column(Integer, ForeignKey('species.id'))  # Relación con Species

    species = relationship("Species", backref="person_species", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "created": self.created,
            "homeworld": self.homeworld_id,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "pic": self.pic,
            "url": self.url,
            "species": self.species_id
        }

# Clase User (Usuario)
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relación con Favorites
    favorites = relationship("Favorites", backref="user_favorites", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

# Clase Favorites (Favoritos)
class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    planet_id = Column(Integer, ForeignKey(Planet.id))  # Relación con Planet
    person_id = Column(Integer, ForeignKey(Persona.id))  # Relación con Persona

    # Relaciones
    user = relationship(User, backref="user_favorites", lazy=True)
    planet = relationship(Planet, backref="planet_favorites", lazy=True)
    person = relationship(Persona, backref="person_favorites", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "person_id": self.person_id
        }

# Clase Starship (Nave Espacial)
class Starship(Base):
    __tablename__ = 'starship'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(50))
    manufacturer = Column(String(100))
    passengers = Column(Integer)
    pilots = relationship("Persona", secondary="starship_pilot", backref="starships")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "passengers": self.passengers
        }

# Tabla intermedia Starship_Pilot (Pilotos de Naves)
class StarshipPilot(Base):
    __tablename__ = 'starship_pilot'
    starship_id = Column(Integer, ForeignKey('starship.id'), primary_key=True)
    persona_id = Column(Integer, ForeignKey('persona.id'), primary_key=True)

# Clase Vehicle (Vehículo)
class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(50))
    manufacturer = Column(String(100))
    passengers = Column(Integer)
    pilots = relationship("Persona", secondary="vehicle_pilot", backref="vehicles")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "passengers": self.passengers
        }

# Tabla intermedia Vehicle_Pilot (Pilotos de Vehículos)
class VehiclePilot(Base):
    __tablename__ = 'vehicle_pilot'
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), primary_key=True)
    persona_id = Column(Integer, ForeignKey('persona.id'), primary_key=True)

# Clase Film (Película)
class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    episode_id = Column(Integer)
    director = Column(String(100))
    producer = Column(String(100))
    release_date = Column(String(50))

    # Relación con Personas, Planetas, Naves y Vehículos
    characters = relationship("Persona", secondary="film_character", backref="films")
    planets = relationship("Planet", secondary="film_planet", backref="films")
    starships = relationship("Starship", secondary="film_starship", backref="films")
    vehicles = relationship("Vehicle", secondary="film_vehicle", backref="films")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.release_date
        }

# Tabla intermedia Film_Character (Personajes en Películas)
class FilmCharacter(Base):
    __tablename__ = 'film_character'
    film_id = Column(Integer, ForeignKey('film.id'), primary_key=True)
    persona_id = Column(Integer, ForeignKey('persona.id'), primary_key=True)

# Tabla intermedia Film_Planet (Planetas en Películas)
class FilmPlanet(Base):
    __tablename__ = 'film_planet'
    film_id = Column(Integer, ForeignKey('film.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)

# Tabla intermedia Film_Starship (Naves en Películas)
class FilmStarship(Base):
    __tablename__ = 'film_starship'
    film_id = Column(Integer, ForeignKey('film.id'), primary_key=True)
    starship_id = Column(Integer, ForeignKey('starship.id'), primary_key=True)

# Tabla intermedia Film_Vehicle (Vehículos en Películas)
class FilmVehicle(Base):
    __tablename__ = 'film_vehicle'
    film_id = Column(Integer, ForeignKey('film.id'), primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), primary_key=True)

# Generar el diagrama
render_er(Base, 'diagram.png')



