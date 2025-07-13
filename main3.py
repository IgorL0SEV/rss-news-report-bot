"""
main3.py
Версия для работы с локальной моделью gemma3 через Ollama.

- Endpoint: http://localhost:11434/v1/chat/completions
- Модель: "gemma3:latest"
- API-ключ не требуется.
- RSS: https://lenta.ru/rss/news
- Логика и структура — как в main.py (OpenAI).
- Отличия: используется requests для обращения к Ollama API, не требуется OPENAI_API_KEY.
- Пример запуска: python main3.py
"""

import os
from dotenv import load_dotenv
import feedparser
import requests
import telegram

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
RSS_URL = "https://lenta.ru/rss/news"
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
# OLLAMA_MODEL = "gemma3:latest"
OLLAMA_MODEL = "phi3:mini"

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан в .env")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID не задан в .env")

def ollama_chat(messages, temperature=0.2):
    """
    messages: [{"role": "system"/"user"/"assistant", "content": "..."}]
    """
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    try:
        response.raise_for_status()
    except Exception as e:
        print("Ollama ответ:", response.text)  # Покажет причину ошибки
        raise
    data = response.json()
    return data["choices"][0]["message"]["content"]

def get_top_news():
    feed = feedparser.parse(RSS_URL)
    news = []
    for entry in feed.entries[:3]:
        news.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", entry.get("description", "")),
            "link": entry.get("link", "")
        })
    return news

def summarize_news(news_list):
    summaries = []
    for news in news_list:
        prompt = (
            f"Новость:\nЗаголовок: {news['title']}\nОписание: {news['summary']}\n\n"
            "Сделай краткое деловое резюме этой новости (1-2 предложения) на русском языке. "
            "Пиши простым и ясным языком для делового человека. Не добавляй ничего лишнего."
        )
        messages = [
            {"role": "system", "content": "Ты деловой ассистент, который кратко резюмирует новости на русском языке."},
            {"role": "user", "content": prompt}
        ]
        summary = ollama_chat(messages)
        summaries.append(summary.strip())
    return summaries

def build_report(summaries):
    report = "📰 Мини-отчёт по последним новостям:\n"
    for idx, summary in enumerate(summaries, 1):
        report += f"{idx}. {summary}\n"
    return report.strip()

def send_telegram_message(token, chat_id, message):
    print(">>> Отправляем отчёт в Telegram...")
    print(f"DEBUG: Сообщение для отправки:\n{message}\n")
    try:
        bot = telegram.Bot(token=token)
        if isinstance(chat_id, str) and chat_id.isdigit():
            chat_id = int(chat_id)
        if not message or not message.strip():
            print("Пустое сообщение, отправка отменена.")
            return
        chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
        for chunk in chunks:
            bot.send_message(chat_id=chat_id, text=chunk)
        print(">>> Сообщение успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")

if __name__ == "__main__":
    print("Запускаем Ollama-магический LLM-пайплайн с делегированием!")
    news = get_top_news()
    print("Топ-3 новости получены.")
    summaries = summarize_news(news)
    print("Сводки новостей сформированы.")
    report = build_report(summaries)
    print("Результат финального отчёта:\n", report)
    send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, report)
    print("Отчёт отправлен в Telegram!")

# Отличия main3.py:
# - Используется Ollama API (requests), а не openai/crewai.
# - Не требуется OPENAI_API_KEY.
# - Модель указывается явно: "gemma3:latest".
# - Не используются функции, vision и другие параметры OpenAI.
# - Вся логика аналогична main.py.
#
# Пример запуска:
# python main3.py
