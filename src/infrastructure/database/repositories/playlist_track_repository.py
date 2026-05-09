from typing import List, Optional, Tuple
from src.domain import PlaylistTrack, PlaylistTrackRepository
from ..models import PlaylistTrackModel


class PeeweePlaylistTrackRepository(PlaylistTrackRepository):
    """Peewee implementation of PlaylistTrackRepository."""

    def save(self, playlist_track: PlaylistTrack) -> PlaylistTrack:
        """Save playlist-track relation."""
        if playlist_track.id is None:
            # Create new
            model = PlaylistTrackModel.create(
                playlist_id=playlist_track.playlist_id,
                track_id=playlist_track.track_id,
                position=playlist_track.position
            )
            playlist_track.id = model.id
        else:
            # Update existing
            model = PlaylistTrackModel.get_by_id(playlist_track.id)
            model.playlist_id = playlist_track.playlist_id
            model.track_id = playlist_track.track_id
            model.position = playlist_track.position
            model.save()

        return playlist_track

    def find_by_playlist_id(self, playlist_id: int) -> List[PlaylistTrack]:
        """Find all tracks in a playlist."""
        models = PlaylistTrackModel.select().where(
            PlaylistTrackModel.playlist_id == playlist_id
        ).order_by(PlaylistTrackModel.position)

        return [self._model_to_entity(model) for model in models]

    def delete_by_playlist_and_track(self, playlist_id: int, track_id: int) -> bool:
        """Remove track from playlist."""
        deleted_count = PlaylistTrackModel.delete().where(
            (PlaylistTrackModel.playlist_id == playlist_id) &
            (PlaylistTrackModel.track_id == track_id)
        ).execute()

        return deleted_count > 0

    def reorder_tracks(self, playlist_id: int, track_orders: List[Tuple[int, int]]) -> bool:
        """Reorder tracks in playlist. track_orders is list of (track_id, new_position)."""
        try:
            for track_id, new_position in track_orders:
                PlaylistTrackModel.update(position=new_position).where(
                    (PlaylistTrackModel.playlist_id == playlist_id) &
                    (PlaylistTrackModel.track_id == track_id)
                ).execute()
            return True
        except Exception:
            return False

    def _model_to_entity(self, model: PlaylistTrackModel) -> PlaylistTrack:
        """Convert Peewee model to domain entity."""
        return PlaylistTrack(
            id=model.id,
            playlist_id=model.playlist_id,
            track_id=model.track_id,
            position=model.position
        )