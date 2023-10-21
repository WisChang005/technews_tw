import datetime

from technews import TechNews


date = datetime.date.today().strftime("%Y-%m-%d")


def test_get_business_today_news():
    today_news = TechNews("business").get_today_news()
    verify_date_format(today_news)


def test_get_ithome_today_news():
    today_news = TechNews("ithome").get_today_news()
    verify_date_format(today_news)


def test_get_inside_today_news():
    today_news = TechNews("inside").get_today_news()
    verify_date_format(today_news)


def test_get_news_by_page():
    news = TechNews("ithome").get_news_by_page(3)
    assert news["timestamp"]
    assert news["news_page_title"]
    assert news["news_contents"]


def verify_date_format(news):
    for _, v in news["news_contents"].items():
        assert date in v["date"] or "hours" in v["date"]
