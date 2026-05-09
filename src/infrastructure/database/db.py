import os
from peewee import SqliteDatabase
from src.domain import DB_PATH


# Initialize database
db = SqliteDatabase(DB_PATH)


def init_database():
    """Initialize database and create tables if they don't exist."""
    from .models import TrackModel, PlaylistModel, PlaylistTrackModel

    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Create tables
    with db:
        db.create_tables([TrackModel, PlaylistModel, PlaylistTrackModel], safe=True)


def close_database():
    """Close database connection."""
    if not db.is_closed():
        db.close()


def get_database():
    """Get database instance."""
    return db