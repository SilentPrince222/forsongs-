# Forsong: Легальный Музыкальный Загрузчик

## Обзор проекта
Forsong - это desktop приложение для поиска и скачивания бесплатной музыки из легальных источников. Приложение ориентировано на творцов, блогеров и обычных пользователей, которым нужна музыка с Creative Commons лицензиями или public domain.

**Основные особенности:**
- Поиск по названию и исполнителю
- Очередь загрузок с прогресс-баром
- Библиотека треков и плейлисты
- Современный GUI на CustomTkinter
- Только легальные источники (без пиратства)

## Требования к системе
- Windows 11 (как указано)
- Python 3.11+
- Минимум 2GB RAM, 500MB дискового пространства
- Интернет-соединение для поиска и загрузки

## Архитектура приложения

### Технологический стек
- **Язык:** Python 3.11+
- **GUI:** CustomTkinter (современная обёртка над Tkinter)
- **Асинхронность:** asyncio + aiohttp для параллельных загрузок
- **Парсинг:** requests + BeautifulSoup4 для статичных страниц, API для динамических
- **База данных:** SQLite + Peewee ORM
- **Метаданные:** mutagen (ID3 теги), Pillow (обложки)
- **Конфигурация:** JSON файлы
- **Сборка:** PyInstaller + Inno Setup

### Файловая структура
```
forsong/
├── main.py                    # Точка входа приложения
├── requirements.txt           # Python зависимости
├── config.json               # Глобальные настройки
├── PLAN.md                   # Этот файл с планом
├── README.md                 # Документация для пользователей
├── .gitignore                # Git игнорируемые файлы
├── src/
│   ├── gui/                  # Графический интерфейс
│   │   ├── app.py            # Главное окно приложения
│   │   ├── tabs/             # Вкладки интерфейса
│   │   │   ├── search_tab.py     # Вкладка поиска
│   │   │   ├── downloads_tab.py  # Вкладка загрузок
│   │   │   ├── library_tab.py    # Вкладка библиотеки
│   │   │   ├── playlists_tab.py  # Вкладка плейлистов
│   │   │   └── settings_tab.py   # Вкладка настроек
│   │   └── widgets/          # Кастомные виджеты
│   │       ├── track_card.py     # Карточка трека
│   │       └── custom_progress.py # Прогресс-бар загрузки
│   ├── core/                 # Ядро приложения
│   │   ├── downloader.py     # Менеджер загрузок (asyncio)
│   │   ├── metadata.py       # Работа с метаданными и обложками
│   │   └── utils.py          # Вспомогательные функции
│   ├── database/             # Работа с базой данных
│   │   ├── db.py             # Инициализация БД
│   │   ├── models.py         # Модели данных (Peewee)
│   │   └── repository.py     # CRUD операции
│   └── sources/              # Парсеры музыкальных источников
│       ├── base_parser.py    # Абстрактный базовый парсер
│       ├── fma_parser.py     # Free Music Archive
│       ├── jamendo_parser.py # Jamendo
│       ├── archive_parser.py # Internet Archive
│       ├── pixabay_parser.py # Pixabay Audio
│       ├── bensound_parser.py # Bensound
│       └── soundclick_parser.py # SoundClick
├── data/                     # Данные приложения
│   ├── db.sqlite3            # База данных SQLite
│   └── settings.json         # Пользовательские настройки
├── downloads/                # Папка для скачанных треков
├── logs/                     # Логи приложения
│   └── app.log               # Файл логов
├── resources/                # Ресурсы (иконки, темы)
│   ├── icons/                # Иконки приложения
│   └── themes/               # Темы интерфейса
└── tests/                    # Тесты
    ├── test_parsers.py       # Тесты парсеров
    ├── test_downloader.py    # Тесты загрузчика
    └── test_database.py      # Тесты БД
```

## Легальные источники музыки

### Поддерживаемые сайты
1. **Free Music Archive (FMA)** - 100k+ треков, API доступен
2. **Jamendo** - 500k+ треков, Creative Commons лицензии, API
3. **Internet Archive** - Миллионы аудиофайлов, public domain, API
4. **Pixabay Audio** - Бесплатные звуковые эффекты и музыка, API
5. **Bensound** - Бесплатная музыка для проектов, простой парсинг HTML
6. **SoundClick** - Артисты сами выкладывают музыку, парсинг страниц
7. **Musopen** - Классическая музыка, public domain

### Исключённые источники (пиратские или проблематичные)
- Muzofond.fm - пиратский контент, заблокирован в РФ
- Tubidy - нарушает авторские права
- Bandcamp - требует авторизации для большинства треков
- SoundCloud - 90% треков не для скачивания
- Generic веб-поиск - ненадёжен, часто возвращает пиратский контент

## Детальный план реализации

### Этап 1: Подготовка (Текущий - Готов)
- ✅ Создание файловой структуры
- ✅ Инициализация Git репозитория
- ✅ Настройка виртуального окружения
- ✅ Установка зависимостей из requirements.txt
- ⏳ Проверка работоспособности базового GUI

### Этап 2: Ядро приложения (Week 1-2)

#### 2.1 База данных
**Файлы:** `src/database/db.py`, `src/database/models.py`, `src/database/repository.py`

**Модели данных:**
```python
class Track(Model):
    title = CharField()
    artist = CharField()
    album = CharField(null=True)
    duration = IntegerField()  # в секундах
    file_path = CharField(unique=True)
    source = CharField()  # 'fma', 'jamendo', etc.
    license = CharField(null=True)  # CC-BY, CC0, etc.
    genre = CharField(null=True)
    year = IntegerField(null=True)
    file_hash = CharField(null=True)  # SHA256 для проверки дублей
    date_added = DateTimeField(default=datetime.now)
    cover_path = CharField(null=True)  # путь к обложке

class Playlist(Model):
    name = CharField(unique=True)
    description = CharField(null=True)
    date_created = DateTimeField(default=datetime.now)

class PlaylistTrack(Model):
    playlist = ForeignKeyField(Playlist, backref='tracks')
    track = ForeignKeyField(Track)
    position = IntegerField()
```

**CRUD операции:**
- `add_track(track_info)` - добавить трек в библиотеку
- `get_all_tracks()` - получить все треки с пагинацией
- `search_tracks(query)` - поиск по названию/артисту
- `delete_track(track_id)` - удалить трек
- `create_playlist(name)` - создать плейлист
- `add_track_to_playlist(playlist_id, track_id)` - добавить трек в плейлист

#### 2.2 Вспомогательные функции
**Файл:** `src/core/utils.py`

**Функции:**
- `sanitize_filename(name: str) -> str` - удаление недопустимых символов для Windows
- `format_duration(seconds: int) -> str` - "185" → "3:05"
- `format_filesize(bytes: int) -> str` - "3145728" → "3.0 MB"
- `calculate_file_hash(filepath: str) -> str` - SHA256 хэш файла
- `ensure_dir(path: str)` - создание директории если не существует
- `get_file_info(filepath: str) -> dict` - размер, дата модификации

#### 2.3 Работа с метаданными
**Файл:** `src/core/metadata.py`

**Функции:**
- `add_metadata(filepath: str, track_info: dict)` - запись ID3 тегов
- `extract_cover_from_url(url: str, output_path: str)` - скачивание обложки
- `generate_text_cover(text: str, output_path: str)` - генерация текстовой обложки
- `get_metadata(filepath: str) -> dict` - чтение метаданных

**Используемые библиотеки:**
- `mutagen` для ID3 тегов (TIT2, TPE1, TALB, TCON, TYER, APIC)
- `Pillow` для обработки изображений обложек

#### 2.4 Менеджер загрузок
**Файл:** `src/core/downloader.py`

**Класс DownloadManager:**
```python
class DownloadManager:
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.queue = asyncio.Queue()
        self.active_tasks = {}  # task_id -> Task
        self.callbacks = {}  # task_id -> callback_function

    async def add_download(self, track_info: dict, output_path: str, callback=None) -> str:
        task_id = str(uuid.uuid4())
        task = DownloadTask(task_id, track_info, output_path, callback)
        await self.queue.put(task)
        return task_id

    async def _worker(self):
        while True:
            task = await self.queue.get()
            asyncio.create_task(self._process_task(task))
            self.queue.task_done()

    async def _process_task(self, task: DownloadTask):
        async with self.semaphore:
            try:
                await self._download_file(task)
                # После загрузки: добавить метаданные, переместить файл, добавить в БД
            except Exception as e:
                # Обработка ошибок, retry logic
                pass

    def cancel_download(self, task_id: str):
        if task_id in self.active_tasks:
            self.active_tasks[task_id].cancel()

    def pause_download(self, task_id: str):
        # Установка флага паузы
        pass

    def resume_download(self, task_id: str):
        # Сброс флага паузы
        pass
```

**Особенности:**
- Поддержка возобновления загрузок (Range requests)
- Прогресс коллбэки для обновления GUI
- Retry с exponential backoff
- Ограничение скорости загрузки (опционально)

### Этап 3: Парсеры источников (Week 1-2)

#### Базовый парсер
**Файл:** `src/sources/base_parser.py`

```python
class BaseParser(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Поиск треков по запросу"""
        pass

    @abstractmethod
    async def get_download_url(self, track_id: str) -> str:
        """Получение прямой ссылки на скачивание"""
        pass

    @staticmethod
    def normalize_track_info(raw_data: dict) -> TrackInfo:
        """Нормализация данных из разных источников"""
        return TrackInfo(
            title=raw_data.get('title', 'Unknown'),
            artist=raw_data.get('artist', 'Unknown'),
            album=raw_data.get('album'),
            duration=raw_data.get('duration', 0),
            genre=raw_data.get('genre'),
            year=raw_data.get('year'),
            license=raw_data.get('license'),
            cover_url=raw_data.get('cover_url'),
            source_url=raw_data.get('source_url'),
            download_url=raw_data.get('download_url')
        )
```

#### Парсер Free Music Archive
**Файл:** `src/sources/fma_parser.py`

**API:** `https://freemusicarchive.org/api/v0/search`
**Параметры:** `?q={query}&limit={limit}&api_key={key}`

**Особенности:**
- JSON ответ с массивом треков
- Поле `track_mp3` содержит прямую ссылку
- Лицензии: Creative Commons

#### Парсер Jamendo
**Файл:** `src/sources/jamendo_parser.py`

**API:** `https://api.jamendo.com/v3.0/tracks/`
**Параметры:** `?client_id={client_id}&format=json&search={query}&limit={limit}`

**Особенности:**
- Требуется бесплатный API ключ
- Поле `audiodownload` содержит ссылку
- Разные лицензии CC

#### Парсер Internet Archive
**Файл:** `src/sources/archive_parser.py`

**API:** `https://archive.org/advancedsearch.php`
**Параметры:** `?q={query}&output=json&rows={limit}&fl[]=identifier,title,creator,description`

**Особенности:**
- Двухэтапный процесс: поиск → получение метаданных файла
- Ссылка: `https://archive.org/download/{identifier}/{filename}.mp3`
- Только public domain контент

### Этап 4: Графический интерфейс (Week 3-4)

#### Главное окно
**Файл:** `src/gui/app.py`

**Структура:**
- Левая панель навигации (иконки вкладок)
- Центральная область с вкладками
- Темная тема, современный дизайн
- Минимальный размер окна 900x600

**Обработка событий:**
- Закрытие окна: корректное завершение asyncio задач
- Переключение вкладок
- Глобальные горячие клавиши

#### Вкладка поиска
**Файл:** `src/gui/tabs/search_tab.py`

**Элементы:**
- Поле поиска (CTkEntry)
- Кнопка "Найти"
- Фильтры: источник, жанр, качество
- Прокручиваемый список результатов
- Карточки треков с кнопками "Скачать" и "Предпросмотр"

**Логика:**
- Поиск в отдельном потоке/asyncio
- Отображение результатов с пагинацией
- Добавление в очередь загрузок

#### Вкладка загрузок
**Файл:** `src/gui/tabs/downloads_tab.py`

**Элементы:**
- Список активных загрузок
- Прогресс-бары с процентами
- Кнопки управления (пауза, отмена, возобновление)
- Статистика: скорость, ETA, размер

**Логика:**
- Обновление UI через коллбэки из DownloadManager
- Уведомления о завершении
- Очистка завершённых загрузок

#### Вкладка библиотеки
**Файл:** `src/gui/tabs/library_tab.py`

**Элементы:**
- Дерево треков (Treeview)
- Фильтры: артист, альбом, жанр
- Поиск в библиотеке
- Контекстное меню: добавить в плейлист, удалить, открыть папку

**Логика:**
- Загрузка из БД с пагинацией
- Сортировка по колонкам
- Экспорт плейлистов

#### Вкладка плейлистов
**Файл:** `src/gui/tabs/playlists_tab.py`

**Элементы:**
- Список плейлистов слева
- Таблица треков плейлиста справа
- Кнопки управления плейлистами
- Drag & drop для переупорядочивания

#### Вкладка настроек
**Файл:** `src/gui/tabs/settings_tab.py`

**Элементы:**
- Выбор папки загрузок
- Настройки загрузки (макс. одновременных, скорость)
- Включение/отключение источников
- Темы интерфейса
- Автозапуск Windows

**Логика:**
- Сохранение в JSON файл
- Валидация настроек
- Применение без перезапуска

### Этап 5: Интеграция и тестирование (Week 5)

#### Интеграция компонентов
- Связывание GUI с ядром через события/коллбэки
- Асинхронная коммуникация между потоками
- Обработка ошибок и исключений
- Логирование всех операций

#### Тестирование
- Unit тесты для парсеров
- Integration тесты для загрузчика
- UI тесты с pytest + customtkinter
- Проверка на реальных данных

### Этап 6: Полировка и оптимизация (Week 6)

#### Производительность
- Кэширование результатов поиска
- Ленивая загрузка изображений
- Оптимизация запросов к API
- Минификация размера сборки

#### Качество кода
- Type hints для всех функций
- Документация (docstrings)
- Линтинг с flake8/black
- Обработка edge cases

#### Функциональность
- Горячие клавиши
- Контекстные меню
- Уведомления Windows
- Автозапуск

### Этап 7: Сборка и релиз (Week 7)

#### PyInstaller
```bash
pyinstaller --onefile --windowed --icon=resources/icons/app.ico --name=Forsong main.py
```

#### Inno Setup
- Установка в Program Files
- Создание ярлыков
- Регистрация автозапуска (опционально)
- Деинсталлятор

#### Релиз на GitHub
- Создание релиза с бинарниками
- README с инструкцией установки
- Скриншоты интерфейса

## Зависимости (requirements.txt)
```
customtkinter>=5.2.0
peewee>=3.16.0
mutagen>=1.46.0
Pillow>=9.5.0
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
aiohttp>=3.8.0
aiosignal>=1.3.0
win10toast>=0.9  # уведомления Windows
pywin32>=305     # для автозапуска
```

## Риски и решения

### Технические риски
1. **Блокировка API** - Решение: кэширование, fallback на другие источники
2. **Изменение структуры сайтов** - Решение: регулярные проверки, обновления парсеров
3. **Ограничения загрузки** - Решение: rate limiting, user-agent rotation
4. **SQLite в многопоточности** - Решение: connection pool, careful locking

### Бизнес-риски
1. **Легальность контента** - Решение: только verified CC лицензии
2. **Авторские права** - Решение: отображение лицензий, disclaimer
3. **Блокировка в РФ** - Решение: VPN опционально, локальные источники

## Метрики успеха
- Стабильная работа всех парсеров
- GUI без зависаний при загрузках
- Корректное сохранение метаданных
- Удобный интерфейс для поиска и управления

## Следующие шаги
1. Проверить requirements.txt и venv
2. Реализовать БД и модели
3. Создать базовый парсер FMA
4. Разработать DownloadManager
5. Построить GUI каркас
6. Интегрировать компоненты
7. Тестирование и полировка
8. Сборка релиза

---

*Последнее обновление: 2026-04-27*
*Версия плана: 2.0*