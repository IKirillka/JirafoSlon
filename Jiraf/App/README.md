# Jiraf - Computer Vision Detection System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Jiraf — это приложение для детектирования объектов на видеопотоке с помощью нейросети YOLOv8. Система включает веб-интерфейс, базу данных и функционал мониторинга в реальном времени.

## 🎯 Возможности

- **Детектирование объектов** — автоматическое распознавание объектов на видео (Box, Sensor, Documentation)
- **Видеопоток в реальном времени** — обработка видео с камеры с конфигурируемым разрешением и FPS
- **Веб-интерфейс** — PySide6 GUI для управления и мониторинга
- **База данных** — хранение данных детектирования в PostgreSQL
- **Сохранение снимков** — сохранение кадров с детектированными объектами
- **Администратор** — система аутентификации с хешированием паролей
- **Мультипроцессорность** — фоновые worker процессы для обработки

## 📋 Требования

- Python 3.10+
- PostgreSQL 12+
- CUDA 12.1 (опционально, для ускорения GPU)
- Вебкамера или другой источник видео

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Miha876/jiraf.git
cd jiraf
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
venv\Scripts\activate  # На Windows
# source venv/bin/activate  # На Linux/macOS
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

Для поддержки GPU (CUDA 12.1):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 4. Конфигурация базы данных

Убедитесь, что PostgreSQL запущен и создана база данных:

```sql
CREATE DATABASE jiraf_db;
```

## ⚙️ Конфигурация

Отредактируйте файл `config.json`:

```json
{
  "camera_index": 1,
  "weights": "path/to/metran_241f-t.pt",
  "conf": 0.8,
  "classes": ["Box", "Sensor", "Documentation"],
  "frame_width": 640,
  "frame_height": 360,
  "db": {
    "host": "localhost",
    "port": 5432,
    "dbname": "jiraf_db",
    "user": "postgres",
    "password": "your_password"
  },
  "snapshot_folder": "C:\\jiraf",
  "fps": 30
}
```

**Параметры:**
- `camera_index` — индекс камеры (0 — встроенная, 1 — внешняя)
- `weights` — путь к файлу весов модели YOLOv8
- `conf` — порог уверенности для детектирования (0-1)
- `frame_width`, `frame_height` — разрешение видео
- `fps` — кадры в секунду

## 📦 Структура проекта

```
jiraf/
├── launcher.py              # Точка входа приложения
├── admin_notifier.py        # Система уведомлений администратору
├── config.json              # Конфигурационный файл
├── requirements.txt         # Зависимости проекта
├── metran_241f-t.pt         # Веса модели YOLOv8
├── app/
│   └── gui.py               # Главное окно и интерфейс (PySide6)
└── jiraf_app/
    ├── __init__.py
    ├── main_window.py       # Логика главного окна
    ├── worker.py            # Фоновые worker процессы
    ├── video.py             # Обработка видеопотока
    ├── detection.py         # Логика детектирования объектов
    ├── database.py          # Работа с PostgreSQL
    ├── configuration.py     # Управление конфигурацией
    └── helpers.py           # Вспомогательные функции
```

## 🏃 Запуск

### Запуск приложения

```bash
python launcher.py
```

Откроется окно приложения с видеопотоком и детектированием объектов.

### Запуск тестов

```bash
# Проверка конфигурации
python -c "from jiraf_app.configuration import load_config; print(load_config())"

# Проверка подключения к БД
python -c "from jiraf_app.database import Database; db = Database(); db.connect()"
```

## 🔧 Использование

1. **Запустить приложение** — `python launcher.py`
2. **Авторизоваться** — введите учетные данные администратора
3. **Запустить детектирование** — нажмите кнопку "Start"
4. **Просмотреть результаты** — результаты сохраняются в базу данных
5. **Скачать снимки** — снимки сохраняются в папку, указанную в `snapshot_folder`

## 📊 Архитектура

- **GUI слой** — PySide6 для пользовательского интерфейса
- **Обработка видео** — OpenCV для захвата и обработки видеопотока
- **Детектирование** — YOLOv8 (Ultralytics) для распознавания объектов
- **Хранилище** — PostgreSQL для сохранения данных
- **Многопроцессорность** — Worker процессы для фоновой обработки

## 🔐 Безопасность

- Пароли администратора хешируются с использованием salt
- Конфиденциальные данные хранятся в `config.json` (не коммитить в git!)
- Используется аутентификация для доступа к функциям

## 📝 Лицензия

MIT License

## 👤 Автор

**Mikhail (waspel)**  
GitHub: [@Miha876](https://github.com/Miha876)

## 🤝 Вклад

Приветствуются pull requests с улучшениями и исправлениями ошибок.

## 📞 Контакты

- Email: mihavladis@gmail.com
- GitHub: https://github.com/Miha876/jiraf

---

**Версия:** 1.0.0  
**Последнее обновление:** Май 2026
