from crewai import Task

class ReportTask(Task):
    def __init__(self, summaries):
        super().__init__(
            description="Объединяет все резюме в финальный отчёт для Telegram",
        )
        self.summaries = summaries

    def run(self):
        report = "📰 Мини-отчёт по последним новостям:\n\n"
        for idx, summary in enumerate(self.summaries, 1):
            report += f"{idx}. {summary}\n\n"
        return report
