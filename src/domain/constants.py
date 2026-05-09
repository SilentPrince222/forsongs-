# Music sources
SOURCES = {
    'fma': 'Free Music Archive',
    'jamendo': 'Jamendo',
    'archive': 'Internet Archive',
    'pixabay': 'Pixabay Audio',
    'bensound': 'Bensound',
    'soundclick': 'SoundClick'
}

# License types
LICENSES = {
    'cc0': 'CC0 (Public Domain)',
    'cc-by': 'CC BY',
    'cc-by-sa': 'CC BY-SA',
    'cc-by-nc': 'CC BY-NC',
    'cc-by-nc-sa': 'CC BY-NC-SA',
    'cc-by-nd': 'CC BY-ND',
    'cc-by-nc-nd': 'CC BY-NC-ND'
}

# Download status
DOWNLOAD_STATUS = {
    'pending': 'Ожидание',
    'downloading': 'Загрузка',
    'paused': 'Приостановлено',
    'completed': 'Завершено',
    'failed': 'Ошибка',
    'cancelled': 'Отменено'
}

# File extensions
SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.flac', '.ogg', '.m4a'}

# Database constants
DB_PATH = 'data/db.sqlite3'
DEFAULT_DOWNLOAD_DIR = 'downloads'
LOGS_DIR = 'logs'
COVER_DIR = 'data/covers'

# API Keys (placeholders - should be in config)
FMA_API_KEY = ''  # Get from https://freemusicarchive.org/api
JAMENDO_CLIENT_ID = ''  # Get from https://developer.jamendo.com/

# Download settings
MAX_CONCURRENT_DOWNLOADS = 3
DEFAULT_TIMEOUT = 30  # seconds
RETRY_ATTEMPTS = 3
CHUNK_SIZE = 8192  # bytes
DOWNLOAD_CHUNK_SIZE = 8192
DOWNLOAD_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# UI constants
WINDOW_TITLE = 'Forsong - Легальный музыкальный загрузчик'
WINDOW_SIZE = '1200x800'
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
THEME = 'dark'
DEFAULT_THEME = 'dark'
DEFAULT_MAX_CONCURRENT = 3
DEFAULT_DOWNLOAD_FOLDER = 'downloads'
DEFAULT_QUALITY = '320'

# Ensure directories exist
from pathlib import Path
for _dir in [Path(DB_PATH).parent, Path(DEFAULT_DOWNLOAD_DIR), Path(LOGS_DIR)]:
    _dir.mkdir(parents=True, exist_ok=True)
del _dir