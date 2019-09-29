import logging

import pytest

from libs import ithome


@pytest.fixture
def news_object():
    return ithome.ITHOME()


@pytest.mark.parametrize("browser_page", [0, 1, 3, 5])
def test_ithome_page_response(news_object, browser_page):
    news_data = news_object.get_news(browser_page)
    _print_first_news_data(news_data)
    assert "timestamp" in news_data
    assert "news_page_title" in news_data
    assert "news_contents" in news_data


def test_ithome_page_load_verification(news_object):
    page1_data = news_object.get_news()
    page_more_data = news_object.get_news(5)
    assert len(page1_data["news_contents"]) < len(page_more_data["news_contents"])


def _print_first_news_data(news_data):
    for news_i in news_data["news_contents"]:
        logging.debug(news_data["news_contents"][news_i])
        break
