class DomainError(Exception):
    """Base class for all domain exceptions."""
    pass


class TrackNotFoundError(DomainError):
    """Raised when a track is not found."""
    pass


class PlaylistNotFoundError(DomainError):
    """Raised when a playlist is not found."""
    pass


class DuplicateTrackError(DomainError):
    """Raised when trying to add a duplicate track."""
    pass


class InvalidTrackDataError(DomainError):
    """Raised when track data is invalid."""
    pass


class ParserError(DomainError):
    """Raised when a parser encounters an error."""
    pass


class DownloadError(DomainError):
    """Raised when download fails."""
    pass


class MetadataError(DomainError):
    """Raised when metadata processing fails."""
    pass


class ValidationError(DomainError):
    """Raised when data validation fails."""
    pass