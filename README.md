# JirafoSlon

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white">
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-Video-5C3EE8?logo=opencv&logoColor=white">
  <img alt="PySide6" src="https://img.shields.io/badge/PySide6-Qt-41CD52?logo=qt&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-Open-brightgreen">
</p>

Десктопное приложение **Слон** для видеомониторинга с 4 камерами.

Основной код лежит в `Slon/App`, а в корне репозитория — только общее описание проекта.

## Features

- 4 камеры в одном окне
- живой видеопоток с настройкой `width`, `height`, `fps`
- сохранение снимков с датой и временем
- админ-панель с паролем
- многопоточный захват видео

## Quick Start

```bash
cd Slon/App
pip install -r requirements.txt
python app.py
```

Запуск с параметрами:

```bash
python app.py --width 640 --height 480 --fps 30
```

## Run Options

- `--cameras 0 1 2 3` - индексы камер
- `--width 640` - ширина потока
- `--height 480` - высота потока
- `--fps 30` - частота кадров

## Project Layout

| Path | Role |
| --- | --- |
| `Slon/App/app.py` | Точка входа |
| `Slon/App/src/main_window.py` | Главное окно |
| `Slon/App/src/camera_worker.py` | Поток захвата видео |
| `Slon/App/src/ui_components.py` | Интерфейс и диалоги |
| `Slon/App/src/utils.py` | Снимки и служебные функции |
| `Slon/App/src/config.py` | Настройки |
| `Slon/App/requirements.txt` | Зависимости |

## Storage

Снимки сохраняются в:

```text
C:/Screenshots/Slon/YYYY-MM-DD/
```

## Admin Access

Пароль: `0098`

