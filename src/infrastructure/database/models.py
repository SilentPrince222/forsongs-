from peewee import Model, CharField, IntegerField, DateTimeField, ForeignKeyField, TextField
from .db import db


class BaseModel(Model):
    """Base model with common fields."""
    class Meta:
        database = db


class TrackModel(BaseModel):
    """Peewee model for tracks."""
    title = CharField()
    artist = CharField()
    album = CharField(null=True)
    duration = IntegerField(default=0)  # in seconds
    file_path = CharField(unique=True)
    source = CharField()  # 'fma', 'jamendo', etc.
    license = CharField(null=True)  # CC-BY, CC0, etc.
    genre = CharField(null=True)
    year = IntegerField(null=True)
    file_hash = CharField(null=True)  # SHA256 for duplicates
    date_added = DateTimeField(default=None)
    cover_path = CharField(null=True)

    class Meta:
        table_name = 'tracks'


class PlaylistModel(BaseModel):
    """Peewee model for playlists."""
    name = CharField(unique=True)
    description = TextField(null=True)
    date_created = DateTimeField(default=None)

    class Meta:
        table_name = 'playlists'


class PlaylistTrackModel(BaseModel):
    """Peewee model for playlist-track relationships."""
    playlist = ForeignKeyField(PlaylistModel, backref='tracks', on_delete='CASCADE')
    track = ForeignKeyField(TrackModel, backref='playlists', on_delete='CASCADE')
    position = IntegerField(default=0)

    class Meta:
        table_name = 'playlist_tracks'
        indexes = (
            (('playlist', 'position'), True),  # Unique position per playlist
        )