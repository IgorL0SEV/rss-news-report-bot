# RSS News Report Bot

AI-мультиагентный бот для автоматического сбора новостей из любой RSS-ленты, их анализа и создания мини-отчёта с отправкой в Telegram.  
**Два режима работы:**  
- **main.py** — мультиагентный пайплайн на CrewAI + OpenAI API (чистая "магия").
- **main2.py** — ручной пайплайн через ProxyAPI.

## 🚀 Возможности

- Автоматический парсинг новостей из выбранного RSS-канала.
- Краткое резюмирование каждой новости на русском языке с помощью LLM.
- Генерация структурированного мини-отчёта.
- Отправка итогового отчёта в Telegram (в виде удобного сообщения).
- Гибкая архитектура: легко расширяется под любые источники/выходы/модели.

## 📂 Структура проекта
```
RSS_NEWS_REPORT_BOT/
├── agents/
│   ├── news_summarizer_task.py
│   ├── report_task.py
│   └── rss_parser_task.py
├── main.py            # CrewAI + OpenAI pipeline
├── main2.py           # ProxyAPI pipeline
├── requirements.txt
├── .gitignore
├── .env
└── test_proxyapi.py

```


## ⚡ Быстрый старт

### 1. Клонировать репозиторий и перейти в папку:

git clone <url>
cd RSS_NEWS_REPORT_BOT

### 2. Создать и активировать виртуальное окружение:
python -m venv venv
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac

### 3. Установи зависимости:
Обычная установка (для пользователей):
pip install -r requirements.txt

Полная установка (идентичное окружение):
pip install -r requirements_full.txt

### 4. Заполнить .env файл (создать, если нет):
```
OPENAI_API_KEY=sk-...              # Только для main.py (OpenAI)
PROXYAPI_KEY=sk-...                # Только для main2.py (ProxyAPI)
TELEGRAM_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
```

### 5. Проверить или изменить адрес RSS-ленты:
RSS_URL = "http://feeds.reuters.com/reuters/topNews"

Можешь указать любую рабочую RSS-ленту.


### 🧠 Как использовать

### 1. CrewAI/OpenAI режим (main.py)

python main.py

Использует CrewAI, агентную архитектуру, официальный OpenAI API.
Максимальная демонстрация современных AI-интеграций.


### 2. ProxyAPI режим (main2.py)

python main2.py
Использует только requests + ProxyAPI (без OpenAI-аккаунта).


### ✍️ Как работает

Парсит 3 свежие новости из выбранной RSS-ленты.
Для каждой новости формирует промпт на русском языке.
LLM (OpenAI или ProxyAPI) делает краткое резюме.
Собирает все summary в структурированный мини-отчёт.
Автоматически отправляет итоговый текст в Telegram.


### 📜 Пример .env

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
PROXYAPI_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_TOKEN=0000000000:AA...    # токен Telegram-бота
TELEGRAM_CHAT_ID=123456789         # ваш Telegram chat_id


### 💡 FAQ и полезное

Модель LLM для ProxyAPI: параметр "model" в main2.py ("gpt-3.5-turbo", "gpt-4o", и т.д.).
Язык ответа: промпты содержат инструкцию “ответ на русском языке”, при необходимости можно усилить формулировку.
Проверка ProxyAPI: есть отдельный файл test_proxyapi.py для диагностики ключа.
requirements.txt: всегда актуализировать через pip freeze > requirements.txt после доустановки библиотек.


### 🛠️ Расширение

Можно добавить любые источники новостей (поддерживаются все RSS).
Легко встраивается в n8n, cron, любые пайплайны.
Можно выводить в другие мессенджеры, email и т.д.
Все агенты и задачи можно кастомизировать (особенно в CrewAI-режиме).

