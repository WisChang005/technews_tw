import datetime

from technews.news_factory import NewsFactory


def test_get_business_today_news():
    date = datetime.date.today().strftime("%Y-%m-%d")
    today_news = NewsFactory.get_today_news("business")
    for _, v in today_news["news_contents"].items():
        assert date in v["date"]


def test_get_orange_today_news():
    date = datetime.date.today().strftime("%Y-%m-%d")
    today_news = NewsFactory.get_today_news("orange")
    for _, v in today_news["news_contents"].items():
        assert date in v["date"]


def test_get_ithome_today_news():
    date = datetime.date.today().strftime("%Y-%m-%d")
    today_news = NewsFactory.get_today_news("ithome")
    for _, v in today_news["news_contents"].items():
        assert date in v["date"]
