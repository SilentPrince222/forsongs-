from typing import List, Optional
from peewee import fn
from src.domain import Track, TrackRepository, TrackNotFoundError, DuplicateTrackError
from ..models import TrackModel


class PeeweeTrackRepository(TrackRepository):
    """Peewee implementation of TrackRepository."""

    def save(self, track: Track) -> Track:
        """Save a track to the database."""
        # Check for duplicate file path
        existing = TrackModel.get_or_none(TrackModel.file_path == track.file_path)
        if existing and existing.id != track.id:
            raise DuplicateTrackError(f"Track with path {track.file_path} already exists")

        # Check for duplicate hash if provided
        if track.file_hash:
            existing_hash = TrackModel.get_or_none(TrackModel.file_hash == track.file_hash)
            if existing_hash and existing_hash.id != track.id:
                raise DuplicateTrackError(f"Track with hash {track.file_hash} already exists")

        if track.id is None:
            # Create new
            model = TrackModel.create(
                title=track.title,
                artist=track.artist,
                album=track.album,
                duration=track.duration,
                file_path=track.file_path,
                source=track.source,
                license=track.license,
                genre=track.genre,
                year=track.year,
                file_hash=track.file_hash,
                date_added=track.date_added,
                cover_path=track.cover_path
            )
            track.id = model.id
        else:
            # Update existing
            model = TrackModel.get_by_id(track.id)
            model.title = track.title
            model.artist = track.artist
            model.album = track.album
            model.duration = track.duration
            model.file_path = track.file_path
            model.source = track.source
            model.license = track.license
            model.genre = track.genre
            model.year = track.year
            model.file_hash = track.file_hash
            model.date_added = track.date_added
            model.cover_path = track.cover_path
            model.save()

        return track

    def find_by_id(self, track_id: int) -> Optional[Track]:
        """Find a track by ID."""
        try:
            model = TrackModel.get_by_id(track_id)
            return self._model_to_entity(model)
        except TrackModel.DoesNotExist:
            return None

    def find_all(self, limit: int = 100, offset: int = 0) -> List[Track]:
        """Find all tracks with pagination."""
        models = TrackModel.select().order_by(TrackModel.date_added.desc()).limit(limit).offset(offset)
        return [self._model_to_entity(model) for model in models]

    def search(self, query: str, limit: int = 20) -> List[Track]:
        """Search tracks by title/artist."""
        # Case-insensitive search
        query_lower = query.lower()
        models = TrackModel.select().where(
            (fn.Lower(TrackModel.title).contains(query_lower)) |
            (fn.Lower(TrackModel.artist).contains(query_lower))
        ).limit(limit)

        return [self._model_to_entity(model) for model in models]

    def delete(self, track_id: int) -> bool:
        """Delete a track by ID."""
        try:
            model = TrackModel.get_by_id(track_id)
            model.delete_instance()
            return True
        except TrackModel.DoesNotExist:
            return False

    def find_by_hash(self, file_hash: str) -> Optional[Track]:
        """Find track by file hash."""
        try:
            model = TrackModel.get(TrackModel.file_hash == file_hash)
            return self._model_to_entity(model)
        except TrackModel.DoesNotExist:
            return None

    def _model_to_entity(self, model: TrackModel) -> Track:
        """Convert Peewee model to domain entity."""
        return Track(
            id=model.id,
            title=model.title,
            artist=model.artist,
            album=model.album,
            duration=model.duration,
            file_path=model.file_path,
            source=model.source,
            license=model.license,
            genre=model.genre,
            year=model.year,
            file_hash=model.file_hash,
            date_added=model.date_added,
            cover_path=model.cover_path
        )