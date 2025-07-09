import os
import feedparser
import requests
from dotenv import load_dotenv
import telegram
import asyncio
from telegram import Bot

load_dotenv()

PROXYAPI_KEY = os.getenv("PROXYAPI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
RSS_URL = "https://habr.com/ru/rss/all/all/?fl=ru"
# RSS_URL = "http://feeds.bbci.co.uk/news/rss.xml"

def parse_rss():
    print(">>> Парсим RSS-ленту...")
    feed = feedparser.parse(RSS_URL)
    news = []
    for entry in feed.entries[:3]:
        news.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary if 'summary' in entry else entry.get('description', '')
        })
    print(f"Найдено {len(news)} новостей.")
    return news

def summarize_news(news_list):
    print(">>> Генерируем рефераты через ProxyAPI...")
    summaries = []
    for news in news_list:
        prompt = (
            "Твоя задача — сделать короткое резюме этой новости в 1-2 предложениях для делового человека. "
            "Ответь строго на русском языке.\n\n"
            f"Заголовок: {news['title']}\n"
            f"Описание: {news['summary']}\n\n"
            "Резюме:"
        )
        payload = {
            "model": "gpt-4.1-nano-2025-04-14",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "temperature": 0.5,
            "max_tokens": 150
        }
        try:
            response = requests.post(
                "https://api.proxyapi.ru/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {PROXYAPI_KEY}"},
                json=payload,
                timeout=30
            )
            res = response.json()
            summary = res["choices"][0]["message"]["content"].strip()
            summaries.append(summary)
            print(f"- [{news['title'][:40]}...] OK")
        except Exception as e:
            print(f"Ошибка при генерации summary: {e}")
            summaries.append("Ошибка при генерации summary.")
    return summaries

def build_report(summaries):
    print(">>> Собираем финальный отчёт...")
    report = "📰 Мини-отчёт по последним новостям:\n\n"
    for idx, summary in enumerate(summaries, 1):
        report += f"{idx}. {summary}\n\n"
    print(">>> Отчёт готов.")
    return report

async def send_telegram_message(token, chat_id, message):
    print(">>> Отправляем отчёт в Telegram через PTB 20+...")
    bot = Bot(token=token)
    chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
    for chunk in chunks:
        await bot.send_message(chat_id=chat_id, text=chunk)
    print(">>> Сообщение успешно отправлено!")



if __name__ == "__main__":
    print("Запускаем мультиагентный пайплайн через ProxyAPI!")
    news_list = parse_rss()
    summaries = summarize_news(news_list)
    report = build_report(summaries)
    print(report)
    # Асинхронный вызов!
    asyncio.run(send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, report))
    print("Отчёт отправлен в Telegram!")
