# RSS News Report Bot

AI-мультиагентный бот для автоматического сбора новостей из любой RSS-ленты, их анализа и создания мини-отчёта с отправкой в Telegram.  
**Три режима работы:**
- **main.py** — мультиагентный пайплайн на CrewAI + OpenAI API.
- **main2.py** — ручной пайплайн через ProxyAPI.
- **main3.py** — работа с локальной LLM через Ollama (например, phi3:mini, gemma3 и др.).

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
│ ├── news_summarizer_task.py
│ ├── report_task.py
│ └── rss_parser_task.py
├── main.py # CrewAI + OpenAI pipeline
├── main2.py # ProxyAPI pipeline
├── main3.py # Ollama (локальная LLM) pipeline
├── requirements.txt
├── .gitignore
├── .env
└── test_proxyapi.py
```


## ⚡ Быстрый старт

### 1. Клонировать репозиторий и перейти в папку:
```
git clone <url>
cd RSS_NEWS_REPORT_BOT
```

### 2. Создать и активировать виртуальное окружение:
```
python -m venv venv

venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac
```

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

Можно указать любую рабочую RSS-ленту.


### 🧠 Как использовать

### 1. CrewAI/OpenAI режим (main.py)

python main.py

Использует CrewAI, агентную архитектуру, официальный OpenAI API.
Максимальная демонстрация современных AI-интеграций.


### 2. ProxyAPI режим (main2.py)

python main2.py
Использует только requests + ProxyAPI (без OpenAI-аккаунта).


### 3. Ollama (локальная LLM) режим (main3.py)

python main3.py

Использует Ollama API (http://localhost:11434/v1/chat/completions).
Модель указывается явно: "phi3:mini" или "gemma3:latest" (переменная OLLAMA_MODEL).
Не требуется API-ключ.
Для работы требуется установленный Ollama и нужная модель (ollama pull phi3:mini или ollama pull gemma3:latest).


### 🖥️ Требования для Ollama/LLM
Операционная система: Windows, Linux, MacOS.
Ollama: https://ollama.com/download
Аппаратные требования:
Для большинства mini/quantized моделей достаточно 8 ГБ RAM и видеокарта с 4–8 ГБ VRAM.
Большие модели (например, gemma3:latest) могут требовать 12+ ГБ VRAM.
Если возникла ошибка cudaMalloc failed: out of memory — выберите более лёгкую модель (phi3:mini, gemma:2b, mistral:7b-q4_K_M и т.п.) или закройте тяжелые приложения.

### ✍️ Как работает

Парсит 3 свежие новости из выбранной RSS-ленты.
Для каждой новости формирует промпт на русском языке.
LLM (OpenAI или ProxyAPI) делает краткое резюме.
Собирает все summary в структурированный мини-отчёт.
Автоматически отправляет итоговый текст в Telegram.


### 📜 Пример .env
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
PROXYAPI_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_TOKEN=0000000000:AA...    # токен Telegram-бота
TELEGRAM_CHAT_ID=123456789         # ваш Telegram chat_id
```

### 💡 FAQ и полезное

Модель LLM для ProxyAPI: параметр "model" в main2.py ("gpt-3.5-turbo", "gpt-4o", и т.д.).
Язык ответа: промпты содержат инструкцию “ответ на русском языке”, при необходимости можно усилить формулировку.
Проверка ProxyAPI: есть отдельный файл test_proxyapi.py для диагностики ключа.
requirements.txt: всегда актуализировать через pip freeze > requirements.txt после доустановки библиотек.

Какую модель выбрать для Ollama?
Рекомендуем "phi3:mini" или любую другую mini/quantized-модель, если у вас менее 12 ГБ VRAM.
Адрес Ollama API:
Всегда http://localhost:11434/v1/chat/completions
Смена модели:
В main3.py параметр OLLAMA_MODEL ("phi3:mini", "gemma3:latest", "mistral:7b-q4_K_M", "llama3:8b-q4_K_M" и др.).
Язык ответа:
Промпты на русском языке, вывод — деловой мини-отчёт для Telegram.
Ошибки с памятью:
Если видите ошибку out of memory — используйте меньшую/квантованную модель или закройте другие приложения, попробуйте перезагрузить ПК.
ProxyAPI:
test_proxyapi.py — для проверки ProxyAPI ключа и подключения.
Расширение:
Легко интегрируется в любые пайплайны (n8n, cron), можно добавить любые источники/выходы.
Смена RSS-ленты:
В каждом main*.py можно указать любой источник в переменной RSS_URL.

### ✉️ Пример запуска main3.py (Ollama):
Скачайте модель для Ollama:
ollama pull phi3:mini
Убедитесь, что Ollama запущен (обычно автоматически после установки).
Запустите:
python main3.py
Бот автоматически соберёт новости, сгенерирует краткое резюме и отправит в Telegram-чат.


### 🛠️ Расширение
Можно добавить любые источники новостей (поддерживаются все RSS).
Легко встраивается в n8n, cron, любые пайплайны.
Можно выводить в другие мессенджеры, email и т.д.
Все агенты и задачи можно кастомизировать (особенно в CrewAI-режиме).

