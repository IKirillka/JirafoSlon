# Jiraf - Computer Vision Detection System

Jiraf - приложение для детектирования объектов на видеопотоке с помощью YOLOv8. GUI на PySide6, хранение событий в PostgreSQL, сохранение снимков и фоновая обработка кадра.

[![Запуск](https://img.shields.io/badge/Запуск-launcher.py-1f6feb?style=for-the-badge)](./Jiraf/App/launcher.py)
[![Конфиг](https://img.shields.io/badge/Конфиг-config.json-2ea043?style=for-the-badge)](./Jiraf/App/config.json)
[![Зависимости](https://img.shields.io/badge/Requirements-requirements.txt-6f42c1?style=for-the-badge)](./Jiraf/App/requirements.txt)
[![Код](https://img.shields.io/badge/Код-Jiraf%2FApp-24292f?style=for-the-badge)](./Jiraf/App/)

## Что умеет

- детектировать Box, Sensor и Documentation
- показывать поток с камеры в реальном времени
- сохранять снимки и писать их в базу
- принимать настройки камеры, весов и FPS из GUI
- защищать админские действия паролем
- запускать обработку кадра в фоне

## Быстрый старт

```bash
git clone https://github.com/IKirillka/JirafoSlon.git
cd JirafoSlon
python -m venv venv
venv\Scripts\activate
pip install -r Jiraf/App/requirements.txt
python Jiraf/App/launcher.py
```

## Конфиг

Основной файл: [Jiraf/App/config.json](./Jiraf/App/config.json)

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

## Требования

- Python 3.10+
- PostgreSQL 12+
- вебкамера или другой источник видео
- CUDA 12.1 опционально

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
