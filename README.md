# 🎵 Forsong - Легальный Музыкальный Загрузчик

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/SilentPrince222/forsongs-)

**Forsong** — это desktop-приложение для поиска и скачивания бесплатной музыки из легальных источников. Приложение ориентировано на творцов, блогеров и обычных пользователей, которым нужна музыка с Creative Commons лицензиями или public domain.

## ✨ Особенности

- 🔍 **Умный поиск** по названию и исполнителю across 6 легальных источников
- 📥 **Очередь загрузок** с прогресс-барами, паузой/возобновлением, отменой
- 📚 **Музыкальная библиотека** с плейлистами
- 🎨 **Современный GUI** на базе CustomTkinter (тёмная/светлая тема)
- ⚖️ **Только легальные источники** (Creative Commons, public domain)
- 📊 **Автоматические метаданные** (ID3 теги) и обложки
- 🚀 **Кроссплатформенность** — Windows, Linux, macOS
- 🧱 **Чистая архитектура** — легко поддерживать и расширять

## 🏗️ Архитектура проекта

Forsong построен по принципам **Clean Architecture** (чистая архитектура) с чётким разделением на слои:

```
src/
├── domain/           # 🔴 Ядро — сущности, интерфейсы, события, исключения, константы
├── application/      # 🟡 Бизнес-логика — сервисы, EventBus
├── infrastructure/   # 🟢 Внешние реализации — БД, HTTP, парсеры, загрузчик, метаданные
└── presentation/     # 🟣 Презентационный слой — GUI, ViewModels, виджеты
```

**Ключевые принципы:**
- Зависимости направлены только **вниз** (верхние слои знают о нижних, но не наоборот)
- Слабая связанность через Dependency Injection и Event Bus
- Каждый слой можно заменить независимо от других
- Все взаимодействия — через события (Pub/Sub)
- Легко тестировать (моки, изоляция слоёв)

Подробнее: [ARCHITECTURE.md](ARCHITECTURE.md)

## 📋 Требования к системе

- **ОС:** Windows 10/11, Linux (Ubuntu, Fedora, Arch и др.), macOS 10.15+
- **Python:** 3.11 или выше (рекомендуется 3.12+)
- **Память:** Минимум 2 GB RAM
- **Место на диске:** 500 MB + место для музыки
- **Интернет:** Для поиска и загрузки музыки

## 🚀 Установка

### Быстрый старт

```bash
# Клонируйте репозиторий
git clone https://github.com/SilentPrince222/forsongs-.git
cd forsongs-

# Создайте виртуальное окружение
python -m venv venv

# Активируйте окружение
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python main.py
```

### Установка из исходников (разработчикам)

```bash
# Убедитесь, что у вас Python 3.11+
python --version

# Установите зависимости
pip install customtkinter peewee mutagen pillow requests aiohttp beautifulsoup4 lxml

# Запуск
python main.py
```

### Сборка исполняемого файла (опционально)

```bash
# Установите PyInstaller
pip install pyinstaller

# Сборка для вашей платформы
pyinstaller --onefile --windowed --name=Forsong main.py
```

## 📖 Как использовать

### Поиск музыки
1. Перейдите на вкладку **"🔍 Поиск"**
2. Введите название песни или исполнителя
3. Выберите источник (или "Все источники")
4. Нажмите **"Найти"** или Enter
5. В результатах нажмите **"⬇️"** для скачивания

### Управление загрузками
- Вкладка **"⬇️ Загрузки"** показывает активные загрузки
- **⏸️** — приостановить, **▶️** — возобновить, **❌** — отменить
- Прогресс-бар, скорость и ETA отображаются в реальном времени

### Библиотека и плейлисты
- Скачанные треки автоматически добавляются в **"📚 Библиотека"**
- Создавайте плейлисты на вкладке **"🎵 Плейлисты"**
- Добавляйте треки в плейлисты из библиотеки (в разработке)

### Настройки
- Папка загрузок по умолчанию
- Максимум одновременных загрузок (1–5)
- Тема интерфейса (тёмная/светлая)
- Включение/отключение источников

## 🎼 Поддерживаемые источники

| Источник | Тип | Лицензия | Примечание |
|----------|-----|----------|------------|
| Free Music Archive (FMA) | API | CC | 100k+ треков |
| Jamendo | API | CC | 500k+ треков, нужен API-ключ |
| Internet Archive | API | Public Domain | Миллионы аудио |
| Pixabay Audio | API | Various | Звуковые эффекты |
| Bensound | Парсинг | Royalty-free | Простой HTML |
| SoundClick | Парсинг | Various | Артисты сами выкладывают |

**Важно:** Для работы Jamendo требуется бесплатный API-ключ (можно получить на [developer.jamendo.com](https://developer.jamendo.com/)). Без ключа источник отключён.

## 🛠️ Разработка

### Структура проекта (Clean Architecture)

```
forsong/
├── main.py                  # Точка входа
├── requirements.txt         # Зависимости
├── ARCHITECTURE.md          # Подробное описание архитектуры
├── PLAN.md                  # План разработки
├── DETAILED_PLAN.md         # Детальный план
├── CHANGELOG.md             # История изменений
├── README.md                # Этот файл
├── test_project.py          # Smoke-тесты
├── data/                    # Динамические данные (БД, настройки)
├── downloads/               # Скачанная музыка
├── logs/                    # Логи
└── src/
    ├── domain/             # Ядро (entities, interfaces, events, exceptions, constants)
    ├── application/        # Сервисы (download, search, metadata, library, playlist, settings)
    ├── infrastructure/     # Реализации (database, sources, http, downloader, metadata)
    └── presentation/       # GUI (app, tabs, viewmodels, widgets, theme)
```

### Запуск тестов

```bash
# Быстрые smoke-тесты (импорты, архитектура)
python test_project.py

# Полный тестовый набор (добавляйте свои тесты в test_project.py)
python -m pytest tests/  # в разработке
```

### Проверка кода

```bash
# Синтаксис
python -m py_compile src/**/*.py

# Статический анализ (добавьте в pre-commit hook)
flake8 src/
mypy src/
```

### Работа с базой данных

База данных SQLite создаётся автоматически в `data/db.sqlite3` при первом запуске. Схема:

- `tracks` — скачанные треки (метаданные, путь, хэш)
- `playlists` — плейлисты
- `playlist_tracks` — связи треков с плейлистами

### Добавление нового источника музыки

1. Создайте класс-парсер в `src/infrastructure/sources/`, унаследовав от `BaseMusicParser`
2. Реализуйте методы `search(query, limit)` и `get_download_url(track_id)`
3. Зарегистрируйте парсер в `di_container.py` (в списке `parsers`)
4. Добавьте источник в `src/domain/constants.py::SOURCES`

## 📦 Зависимости

Основные библиотеки:
- `customtkinter>=5.2.0` — современный GUI
- `peewee>=3.16.0` — ORM для SQLite
- `mutagen>=1.46.0` — работа с метаданными (ID3)
- `Pillow>=9.5.0` — обработка изображений (обложки)
- `requests>=2.28.0` — HTTP-запросы (синхронные)
- `aiohttp>=3.8.0` — асинхронные загрузки
- `beautifulsoup4>=4.11.0` — парсинг HTML
- `lxml>=4.9.0` — быстрый XML/HTML парсер

## 🤝 Вклад в проект

Мы приветствуем вклад!

1. **Fork** репозитория
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. **Push** в branch (`git push origin feature/AmazingFeature`)
5. Создайте **Pull Request**

### Типыcontributions:
- 🐛 Исправление багов
- ✨ Новые функции
- 📚 Документация
- 🎨 UI/UX улучшения
- 🧪 Тесты
- 🔧 Рефакторинг

## 📄 Лицензия

MIT License — см. файл [LICENSE](LICENSE).

## ⚠️ Важные замечания

### Легальность
- Forsong скачивает **только легальную музыку** из проверенных источников
- Все треки имеют соответствующие лицензии (Creative Commons, public domain)
- Приложение **не содержит пиратского контента**
- Пользователь обязан проверять лицензии при коммерческом использовании

### Поддержка платформ
- Приложение официально поддерживает Windows, Linux и macOS
- Для Linux-уведомлений может потребоваться `libnotify` (`sudo apt install libnotify-bin`)
- На Linux рекомендуется Python 3.12+ для совместимости с aiohttp

## 📞 Поддержка

- 🐛 **Issues:** [GitHub Issues](https://github.com/SilentPrince222/forsongs-/issues)
- 📖 **Wiki:** [Документация](https://github.com/SilentPrince222/forsongs-/wiki)
- 💬 **Discussions:** [Обсуждения](https://github.com/SilentPrince222/forsongs-/discussions)

## 🙏 Благодарности

- [Free Music Archive](https://freemusicarchive.org/) — за API
- [Jamendo](https://www.jamendo.com/) — за музыкальную платформу
- [Internet Archive](https://archive.org/) — за сохранение цифрового наследия
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — за красивый GUI
- [aiohttp](https://github.com/aio-libs/aiohttp) — за асинхронные HTTP-запросы
- [mutagen](https://github.com/quodlibet/mutagen) — за работу с аудио-метаданными

---

⭐ **Если проект оказался полезным, поставьте звезду на GitHub!**

*Создано с ❤️ для музыкантов и творцов*