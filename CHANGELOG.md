
## 2026-05-10 04:06:02 - Automated Update

### File Changes:
- DELETED: src/database/repository.py
- DELETED: src/database/db.py
- DELETED: src/database/__init__.py
- DELETED: src/database/models.py
- DELETED: src/sources/archive_parser.py
- DELETED: src/sources/pixabay_parser.py
- DELETED: src/sources/bensound_parser.py
- DELETED: src/sources/__init__.py
- DELETED: src/sources/fma_parser.py
- DELETED: src/sources/jamendo_parser.py
- DELETED: src/sources/base_parser.py
- DELETED: src/sources/soundclick_parser.py


## 2026-05-10 04:04:11 - Automated Update

### File Changes:
- MODIFIED: src/presentation/di_container.py
- MODIFIED: src/presentation/app.py
- NEW: src/presentation/theme_manager.py
- NEW: src/presentation/viewmodels/playlists_viewmodel.py
- NEW: src/presentation/viewmodels/library_viewmodel.py
- NEW: src/presentation/viewmodels/settings_viewmodel.py
- NEW: src/presentation/widgets/track_card.py
- NEW: src/presentation/widgets/__init__.py
- NEW: src/presentation/widgets/custom_progress.py
- NEW: src/presentation/tabs/search_tab.py
- NEW: src/presentation/tabs/settings_tab.py
- NEW: src/presentation/tabs/__init__.py
- NEW: src/presentation/tabs/playlists_tab.py
- NEW: src/presentation/tabs/library_tab.py
- NEW: src/presentation/tabs/downloads_tab.py
- MODIFIED: src/infrastructure/__init__.py
- MODIFIED: src/infrastructure/downloader.py
- NEW: src/infrastructure/metadata/cover_downloader.py
- NEW: src/infrastructure/metadata/processor.py
- MODIFIED: src/infrastructure/database/repositories/track_repository.py
- MODIFIED: src/infrastructure/database/repositories/playlist_repository.py
- MODIFIED: src/infrastructure/database/repositories/playlist_track_repository.py
- MODIFIED: src/domain/constants.py
- MODIFIED: src/shared/utils.py
- MODIFIED: src/application/__init__.py
- NEW: src/application/services/settings_service.py
- NEW: src/application/services/library_service.py
- NEW: src/application/services/playlist_service.py
- MODIFIED: src/application/services/metadata_service.py
- MODIFIED: src/application/services/download_service.py
- DELETED: src/core/constants.py
- DELETED: src/core/utils.py
- DELETED: src/core/__init__.py
- DELETED: src/core/downloader.py
- DELETED: src/core/metadata.py
- DELETED: src/gui/__init__.py
- DELETED: src/gui/app.py
- DELETED: src/gui/widgets/track_card.py
- DELETED: src/gui/widgets/__init__.py
- DELETED: src/gui/widgets/custom_progress.py
- DELETED: src/gui/tabs/search_tab.py
- DELETED: src/gui/tabs/settings_tab.py
- DELETED: src/gui/tabs/__init__.py
- DELETED: src/gui/tabs/playlists_tab.py
- DELETED: src/gui/tabs/library_tab.py
- DELETED: src/gui/tabs/downloads_tab.py

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- (待添加新功能)

### Changed
- (待添加 изменения)

### Fixed
- (待添加 исправления)

---

## [0.2.0] - 2026-05-02 — Complete Clean Architecture Refactor

### 🏗️ Architecture
- **Полный переход на Clean Architecture** (4 слоя: Domain, Application, Infrastructure, Presentation)
- Удалены дублирующие слои: `src/core/` и устаревший `src/gui/`
- Единый источник констант: `src/domain/constants.py`
- Общие утилиты: `src/shared/utils.py`
- Event-driven коммуникация через **EventBus** (Pub/Sub)
- **Dependency Injection** контейнер в `presentation/di_container.py`
- Чёткие границы слоёв: зависимости только вниз

### 🎯 Presentation Layer (новый)
- Переписаны все 5 вкладок на MVVM:
  - `SearchTab` — поиск с фильтрацией источника
  - `DownloadsTab` — управление загрузками (пауза/возобновление/отмена)
  - `LibraryTab` — библиотека треков
  - `PlaylistsTab` — управление плейлистами
  - `SettingsTab` — настройки приложения
- **ViewModels** отделяют UI от бизнес-логики:
  - `SearchViewModel`, `DownloadsViewModel`, `LibraryViewModel`, `PlaylistsViewModel`, `SettingsViewModel`
- Кастомные виджеты:
  - `TrackCard` — карточка трека с кнопкой скачивания
  - `CustomProgressBar` — прогресс-бар со скоростью и ETA
- `ThemeManager` — управление светлой/тёмной темой

### ⚙️ Application Layer (переписан)
- **DownloadService** — управление загрузками, координация с DownloadManager, обработка событий
- **SearchService** — поиск по всем источникам, параллельные запросы
- **MetadataService** — обработка ID3 тегов и обложек (mutagen + Pillow)
- **LibraryService** — CRUD операции с библиотекой
- **PlaylistService** — управление плейлистами и связями treck→playlist
- **SettingsService** — конфигурация (JSON-файл)
- **ParserManager** — агрегация парсеров, выбор источника

### 🛠️ Infrastructure Layer (улучшен)
- **DownloadManager** полностью переработан:
  - Поддержка pause/resume через HTTP Range requests
  - Retry с exponential backoff (3 попытки)
  - Прогресс-коллбэки с расчётом скорости и ETA
  - Отмена загрузки с очисткой частичного файла
  - Автоматическое создание директорий
- **MetadataProcessor** — обёртка над mutagen для ID3 тегов
- **CoverDownloader** — скачивание и генерация текстовых обложек (Pillow)
- **HTTP Client** — `AioHttpClient` реализует `HttpClient` интерфейс
- **Repositories** — Peewee ORM реализации `TrackRepository`, `PlaylistRepository`, `PlaylistTrackRepository`
- **Parsers** — 6 источников (FMA, Jamendo, Internet Archive, Pixabay, Bensound, SoundClick)

### 🎵 Domain Layer (стабилен)
- Сущности: `Track`, `Playlist`, `PlaylistTrack`, `TrackInfo`, `DownloadTask`
- Интерфейсы: `TrackRepository`, `MusicParser`, `HttpClient`, `EventBus`, `Logger`
- События и команды: `SearchStartedEvent`, `DownloadCompletedEvent`, `TrackAddedEvent`, и т.д.
- Исключения: `DomainError`, `DownloadError`, `ParserError` и др.
- Константы: все пути, настройки, лицензии, источники

### 🐧 Linux Support
- Удалены Windows-зависимости: `win10toast`, `pywin32` из `requirements.txt`
- Приложение успешно запускается на Linux (Ubuntu 24.04, Python 3.14)
- Исправлены пути (используется `pathlib.Path`)
- Создание директорий: `data/`, `downloads/`, `logs/` автоматически

### 🧪 Testing
- `test_project.py` — smoke-тесты для проверки архитектуры и импортов
- Все 5 тестов проходят:
  - Domain layer imports
  - Application layer imports
  - Shared utilities
  - Architecture separation (запрещённые импорты)
  - Infrastructure structure

### 🐛 Bug Fixes
- Fix: относительные импорты в репозиториях (`from ..models import`)
- Fix: несуществующие обработчики событий в `app.py` (`_on_search_started` → `_on_search_started_ui`)
- Fix: двойной вызов `container.startup()` (удалён из `main.py`, оставлен в фоновом потоке)
- Fix: `DownloadManager.pause/resume` (ранее были заглушками)
- Fix: `MetadataService` теперь получает `track_repository` через DI
- Fix: `DownloadService` корректно формирует полный путь к файлу и добавляет трек в библиотеку
- Fix: дублирование кода между `src/core/` и `src/shared/` (удалён `src/core/`)
- Fix: устаревший GUI слой `src/gui/` полностью удалён

### 📚 Documentation
- Обновлён `README.md`: архитектура, структура, инструкции для Linux
- Обновлён `ARCHITECTURE.md`: фактическая структура `presentation/` вместо `gui/`
- Добавлены комментарии в код (где необходимо)

### 🔄 Compatibility
- Обратная совместимость: DataBase schema сохраняется
- Конфигурационный файл `config.json` совместим
- Все парсеры работают как раньше (plus исправления)

---

## [0.1.0] - 2026-05-01 (Initial Development)

### Added
- Базовая файловая структура
- Простой GUI на CustomTkinter (до рефакторинга)
- Первые версии парсеров (FMA, Jamendo, Archive)
- Загрузчик на asyncio (базовая версия)
- Peewee ORM для SQLite
- Метаданные (mutagen) и обложки (Pillow)
- Quality check system (test_project.py, check_quality.sh)
