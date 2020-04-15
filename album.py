import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    
    __tablename__ = "album"

    id = db.Column(db.INTEGER, primary_key=True)
    year = db.Column(db.INTEGER)
    artist = db.Column(db.TEXT)
    genre = db.Column(db.TEXT)
    album = db.Column(db.TEXT)


def connect_db():
   
    engine = db.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
       
    return albums

def save(year, artist, genre, album):
    assert isinstance(year, int), "Incorrect date"
    assert isinstance(artist, str), "Incorrect artist"
    assert isinstance(genre, str), "Incorrect genre"
    assert isinstance(album, str), "Incorrect album"

    session = connect_db()
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album:
        raise AlreadyExists("Album already exists and has #{}".format(saved_album.id))

    album = Album(
        year = year,
        artist = artist,
        genre = genre,
        album = album
    )    
    session.add(album)
    session.commit()
    return album