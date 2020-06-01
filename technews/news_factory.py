import time
import datetime

from technews.business_next import BusinessNext
from technews.tech_orange import TechOrange
from technews.ithome import iThome


class NewsFactory:

    @classmethod
    def get_today_news(cls, news_name: str):
        """
        Returns:
            "timestamp": "1231231255",
            "news_page_title": "222222",
            "news_contents": "111111",
        """
        date = datetime.date.today().strftime("%Y-%m-%d")
        news_obj = cls._init_news_object(news_name)
        all_news = news_obj.get_news(3)
        today_news = {}
        for k, v in all_news["news_contents"].items():
            if date in v["date"]:
                today_news[k] = v

        news_tpl = {
            "timestamp": time.time(),
            "news_page_title": all_news["news_page_title"],
            "news_contents": today_news
        }
        return news_tpl

    @classmethod
    def _init_news_object(cls, news_name: str):
        news_obj = {
            "business": BusinessNext,
            "orange": TechOrange,
            "ithome": iThome
        }
        if news_name not in news_obj:
            raise ValueError(f"No supported news name [{news_name}]")
        return news_obj[news_name]()
