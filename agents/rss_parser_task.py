import feedparser
from crewai import Task

class RSSParserTask(Task):
    def __init__(self, rss_url, top_n=3):
        super().__init__(
            description="Парсит топ-3 новости из RSS-ленты",
        )
        self.rss_url = rss_url
        self.top_n = top_n

    def run(self):
        feed = feedparser.parse(self.rss_url)
        news = []
        for entry in feed.entries[:self.top_n]:
            news.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary if 'summary' in entry else entry.get('description', '')
            })
        return news

