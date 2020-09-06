import datetime

from technews import TechNews


def test_get_business_today_news():
    date = datetime.date.today().strftime("%Y-%m-%d")
    today_news = TechNews("business").get_today_news()
    for _, v in today_news["news_contents"].items():
        assert date in v["date"]


def test_get_orange_today_news():
    date = datetime.date.today().strftime("%Y-%m-%d")
    today_news = TechNews("orange").get_today_news()
    for _, v in today_news["news_contents"].items():
        assert date in v["date"]


def test_get_ithome_today_news():
    date = datetime.date.today().strftime("%Y-%m-%d")
    today_news = TechNews("ithome").get_today_news()
    for _, v in today_news["news_contents"].items():
        assert date in v["date"]


def test_get_inside_today_news():
    date = datetime.date.today().strftime("%Y-%m-%d")
    today_news = TechNews("inside").get_today_news()
    for _, v in today_news["news_contents"].items():
        assert date in v["date"]


def test_get_news_by_page():
    news = TechNews("ithome").get_news_by_page(3)
    assert news["timestamp"]
    assert news["news_page_title"]
    assert news["news_contents"]
