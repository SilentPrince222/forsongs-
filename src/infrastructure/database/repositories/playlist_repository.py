from typing import List, Optional
from src.domain import Playlist, PlaylistRepository, PlaylistNotFoundError
from ..models import PlaylistModel


class PeeweePlaylistRepository(PlaylistRepository):
    """Peewee implementation of PlaylistRepository."""

    def save(self, playlist: Playlist) -> Playlist:
        """Save a playlist."""
        if playlist.id is None:
            # Create new
            model = PlaylistModel.create(
                name=playlist.name,
                description=playlist.description,
                date_created=playlist.date_created
            )
            playlist.id = model.id
        else:
            # Update existing
            model = PlaylistModel.get_by_id(playlist.id)
            model.name = playlist.name
            model.description = playlist.description
            model.date_created = playlist.date_created
            model.save()

        return playlist

    def find_by_id(self, playlist_id: int) -> Optional[Playlist]:
        """Find playlist by ID."""
        try:
            model = PlaylistModel.get_by_id(playlist_id)
            return self._model_to_entity(model)
        except PlaylistModel.DoesNotExist:
            return None

    def find_all(self) -> List[Playlist]:
        """Find all playlists."""
        models = PlaylistModel.select().order_by(PlaylistModel.date_created.desc())
        return [self._model_to_entity(model) for model in models]

    def delete(self, playlist_id: int) -> bool:
        """Delete playlist by ID."""
        try:
            model = PlaylistModel.get_by_id(playlist_id)
            model.delete_instance()
            return True
        except PlaylistModel.DoesNotExist:
            return False

    def _model_to_entity(self, model: PlaylistModel) -> Playlist:
        """Convert Peewee model to domain entity."""
        return Playlist(
            id=model.id,
            name=model.name,
            description=model.description,
            date_created=model.date_created
        )