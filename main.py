import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, Process
from crewai.tools import tool
import feedparser
import telegram
import asyncio
from telegram import Bot

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
RSS_URL = "http://feeds.bbci.co.uk/news/rss.xml"
# RSS_URL = "http://feeds.reuters.com/reuters/topNews"
# RSS_URL = "https://lenta.ru/rss/news"
# RSS_URL = "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"

# Проверка переменных окружения
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не задан в .env")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан в .env")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID не задан в .env")

# --- Агент 1: RSS-парсер (TOOL) ---
rss_agent = Agent(
    role="RSS-парсер",
    goal="Собрать топ-3 новости из RSS-ленты.",
    backstory="Супероперативный бот-парсер.",
    allow_delegation=False,
    model="gpt-4.1-nano-2025-04-14"
)

@tool("get_top_news")
def get_top_news(_=None):
    """Получить топ-3 новости из RSS-ленты"""
    feed = feedparser.parse(RSS_URL)
    news = []
    for entry in feed.entries[:3]:
        news.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", entry.get("description", "")),
            "link": entry.get("link", "")
        })
    return news

# --- Агент 2: AI-референт ---
summarizer_agent = Agent(
    role="AI-референт",
    goal="Кратко и по-деловому резюмировать каждую новость.",
    backstory="Всегда выделяет главное и пишет ясно и лаконично.",
    allow_delegation=False,
    model="gpt-4.1-nano-2025-04-14"
)

# --- Агент 3: AI-редактор-дайджестолог ---
report_agent = Agent(
    role="AI-редактор",
    goal="Объединить summary новостей в структурированный мини-отчёт.",
    backstory="Создаёт мини-дайджесты для занятых руководителей.",
    allow_delegation=False,
    model="gpt-4.1-nano-2025-04-14"
)

# --- Step 1. Task: Получить топ-3 новости (tool+LLM magic) ---
rss_task = Task(
    description=(
        f"Используй встроенный инструмент (tool), чтобы получить список из 3 последних новостей с RSS-ленты {RSS_URL}. "
        "Верни их как список словарей (заголовок, описание, ссылка)."
    ),
    agent=rss_agent,
    expected_output="Список из трёх новостей, каждая — словарь с title, summary, link.",
    tools=[get_top_news],  # Передаём функцию, декорированную @tool
    input=None
)

# --- Step 2. Task: Реферировать каждую новость ---
summarizer_task = Task(
    description=(
        "Для каждой новости из предыдущего шага напиши краткое деловое резюме (1-2 предложения) на русском языке. "
        "Пиши простым и ясным языком для делового человека. "
        "Верни список из трёх summary на русском, не добавляй ничего лишнего."
    ),
    agent=summarizer_agent,
    expected_output="Список из трёх кратких summary на русском языке.",
    input=lambda: rss_task.output
)

# --- Step 3. Task: Собрать финальный отчёт ---
report_task = Task(
    description=(
        "Объедини все summary новостей в мини-отчёт для Telegram на русском языке: "
        "добавь заголовок '📰 Мини-отчёт по последним новостям:', после него сделай нумерованный список. "
        "Весь текст должен быть на русском языке."
    ),
    agent=report_agent,
    expected_output="Финальный текст мини-отчёта для Telegram на русском языке.",
    input=lambda: summarizer_task.output
)

# --- Crew pipeline ---
crew = Crew(
    agents=[rss_agent, summarizer_agent, report_agent],
    tasks=[rss_task, summarizer_task, report_task],
    process=Process.sequential,
    openai_api_key=OPENAI_API_KEY
)


async def send_telegram_message(token, chat_id, message):
    print(">>> Отправляем отчёт в Telegram через PTB 20+...")
    bot = Bot(token=token)
    chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
    for chunk in chunks:
        await bot.send_message(chat_id=chat_id, text=chunk)
    print(">>> Сообщение успешно отправлено!")



if __name__ == "__main__":
    print("Запускаем CrewAI-магический LLM-пайплайн с делегированием!")
    results = crew.kickoff()
    if not isinstance(results, str):
        results = str(results)
    print("Результат финального отчёта:\n", results)
    asyncio.run(send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, results))
    print("Отчёт отправлен в Telegram!")



