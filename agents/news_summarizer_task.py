import requests
from crewai import Task
import os
from dotenv import load_dotenv

load_dotenv()
PROXYAPI_KEY = os.getenv("PROXYAPI_KEY")

class NewsSummarizerTask(Task):
    def __init__(self, news_list):
        super().__init__(
            description="Делает краткий реферат каждой новости через ProxyAPI",
        )
        self.news_list = news_list

    def run(self):
        summaries = []
        for news in self.news_list:
            prompt = (
                "Твоя задача — сделать короткое резюме этой новости в 1-2 предложениях для делового человека:\n\n"
                f"Заголовок: {news['title']}\n"
                f"Описание: {news['summary']}\n\n"
                "Резюме:"
            )
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "temperature": 0.5,
                "max_tokens": 150
            }
            response = requests.post(
                "https://api.proxyapi.ru/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {PROXYAPI_KEY}"},
                json=payload,
                timeout=30
            )
            res = response.json()
            summary = res["choices"][0]["message"]["content"].strip()
            summaries.append(summary)
        return summaries

