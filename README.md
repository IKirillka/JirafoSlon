# Jiraf - Computer Vision Detection System

Jiraf - приложение для детектирования объектов на видеопотоке с помощью YOLOv8. Интерфейс на PySide6, хранение событий в PostgreSQL, сохранение снимков и фоновая обработка кадра.

## Возможности

- детектирование объектов Box, Sensor, Documentation
- просмотр видеопотока в реальном времени
- управление камерой, весами и параметрами из GUI
- сохранение снимков в папку и в базу
- админ-доступ по паролю
- фоновые worker-потоки для обработки видео

## Требования

- Python 3.10+
- PostgreSQL 12+
- вебкамера или другой источник видео
- CUDA 12.1 опционально

## Установка

```bash
git clone https://github.com/IKirillka/JirafoSlon.git
cd JirafoSlon
python -m venv venv
venv\Scripts\activate
pip install -r Jiraf/App/requirements.txt
```

## Конфигурация

Основной конфиг лежит в `Jiraf/App/config.json`.

```json
{
  "camera_index": 0,
  "weights": "metran_241f-t.pt",
  "conf": 0.8,
  "classes": ["Box", "Sensor", "Documentation"],
  "frame_width": 640,
  "frame_height": 360,
  "db": {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password"
  },
  "snapshot_folder": "C:\\jiraf",
  "fps": 30
}
```

## Запуск

```bash
python Jiraf/App/launcher.py
```

## Структура

```text
Jiraf/App/
├── launcher.py
├── config.json
├── admin_notifier.py
├── app/
│   └── gui.py
└── jiraf_app/
    ├── configuration.py
    ├── database.py
    ├── detection.py
    ├── helpers.py
    ├── main_window.py
    ├── video.py
    └── worker.py
```

## Автор

Mikhail (waspel)
