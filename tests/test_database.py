import os
import pytest
from datetime import datetime
from peewee import SqliteDatabase
from src.infrastructure.database.models import TrackModel, PlaylistModel, PlaylistTrackModel

# Create an in-memory database for testing
test_db = SqliteDatabase(':memory:')

# Bind models to the test database
MODELS = [TrackModel, PlaylistModel, PlaylistTrackModel]

@pytest.fixture(autouse=True)
def setup_database():
    """Setup and teardown the in-memory database for each test."""
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)
    yield
    test_db.drop_tables(MODELS)
    test_db.close()

def test_create_track():
    track = TrackModel.create(
        title="Test Song",
        artist="Test Artist",
        duration=120,
        file_path="/path/to/test.mp3",
        source="test",
        date_added=datetime.now()
    )
    assert track.id is not None
    assert track.title == "Test Song"
    assert track.artist == "Test Artist"
    
def test_create_playlist():
    playlist = PlaylistModel.create(
        name="My Favorites",
        description="A list of my favorite songs",
        date_created=datetime.now()
    )
    assert playlist.id is not None
    assert playlist.name == "My Favorites"
    
def test_add_track_to_playlist():
    track = TrackModel.create(
        title="Test Song",
        artist="Test Artist",
        file_path="/path/to/test.mp3",
        source="test",
        date_added=datetime.now()
    )
    playlist = PlaylistModel.create(
        name="My Favorites",
        date_created=datetime.now()
    )
    playlist_track = PlaylistTrackModel.create(
        playlist=playlist,
        track=track,
        position=1
    )
    assert playlist_track.id is not None
    assert playlist_track.playlist.id == playlist.id
    assert playlist_track.track.id == track.id
    
def test_unique_file_path_constraint():
    TrackModel.create(
        title="Test Song 1",
        artist="Test Artist",
        file_path="/path/to/test.mp3",
        source="test",
        date_added=datetime.now()
    )
    from peewee import IntegrityError
    with pytest.raises(IntegrityError):
        TrackModel.create(
            title="Test Song 2",
            artist="Test Artist",
            file_path="/path/to/test.mp3",
            source="test",
            date_added=datetime.now()
        )