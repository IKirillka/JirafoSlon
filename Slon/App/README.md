# Слон

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white">
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-Video-5C3EE8?logo=opencv&logoColor=white">
  <img alt="PySide6" src="https://img.shields.io/badge/PySide6-Qt-41CD52?logo=qt&logoColor=white">
</p>

Десктопное приложение для видеомониторинга с 4 камерами.

## Возможности

- 4 камеры в одном окне
- живой видеопоток
- настройка `width`, `height`, `fps`
- сохранение снимков с датой и временем
- админ-панель с паролем

## Запуск

```bash
pip install -r requirements.txt
python app.py
```

Запуск с параметрами:

```bash
python app.py --width 640 --height 480 --fps 30
```

## Параметры

- `--cameras 0 1 2 3` - индексы камер
- `--width 640` - ширина потока
- `--height 480` - высота потока
- `--fps 30` - частота кадров

## Структура

- `app.py` - точка входа
- `src/main_window.py` - главное окно
- `src/camera_worker.py` - поток видеозахвата
- `src/ui_components.py` - интерфейс и диалоги
- `src/utils.py` - снимки и утилиты
- `src/config.py` - настройки
- `requirements.txt` - зависимости

## Снимки

Файлы сохраняются в:

```text
C:/Screenshots/Slon/YYYY-MM-DD/
```

## Админ-доступ

Пароль: `0098`

