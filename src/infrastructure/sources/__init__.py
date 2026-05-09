from .base_parser import BaseMusicParser
from .fma_parser import FMAMusicParser
from .jamendo_parser import JamendoMusicParser
from .archive_parser import InternetArchiveMusicParser
from .pixabay_parser import PixabayAudioParser
from .bensound_parser import BensoundMusicParser
from .soundclick_parser import SoundClickMusicParser

__all__ = [
    'BaseMusicParser',
    'FMAMusicParser',
    'JamendoMusicParser',
    'InternetArchiveMusicParser',
    'PixabayAudioParser',
    'BensoundMusicParser',
    'SoundClickMusicParser'
]