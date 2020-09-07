import time
import datetime

from technews.crawlers.business_next import BusinessNext
from technews.crawlers.tech_orange import TechOrange
from technews.crawlers.ithome import iThome
from technews.crawlers.inside import Inside


class TechNews:

    def __init__(self, news_name: str):
        self.news_name = news_name
        self.news_obj = self._init_news_object()

    def _init_news_object(self):
        news_obj = {
            "business": BusinessNext,
            "orange": TechOrange,
            "ithome": iThome,
            "inside": Inside
        }
        if self.news_name not in news_obj:
            raise ValueError(f"No supported news name [{self.news_name}]")
        return news_obj[self.news_name]()

    def get_news_by_page(self, page):
        return self.news_obj.get_news(page)

    def get_today_news(self):
        """
        Returns:
            "timestamp": "1231231255",
            "news_page_title": "222222",
            "news_contents": {"111111"},
            "news_counts": 111
        """
        date = datetime.date.today().strftime("%Y-%m-%d")
        all_news = self.news_obj.get_news(3)
        today_news = {}
        for k, v in all_news["news_contents"].items():
            if date in v["date"] or "hours" in v["date"]:
                today_news[k] = v

        news_tpl = {
            "timestamp": time.time(),
            "news_page_title": all_news["news_page_title"],
            "news_contents": today_news,
            "news_counts": len(today_news)
        }
        return news_tpl
