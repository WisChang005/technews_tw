import json
import logging

import pytest

from technews.crawlers import business_next


business = business_next.BusinessNext()


@pytest.mark.parametrize("browser_page", [0, 1, 3, 5])
def test_business_next_page_response(browser_page):
    news_data = business.get_news(browser_page)
    _print_first_news_data(news_data)
    assert "timestamp" in news_data
    assert "news_page_title" in news_data
    assert "news_contents" in news_data


def test_business_next_page_load_verification():
    page1_data = business.get_news()
    page_more_data = business.get_news(5)
    assert len(page1_data["news_contents"]) <= len(page_more_data["news_contents"])


def _print_first_news_data(news_data):
    for news_i in news_data["news_contents"]:
        logging.debug("News Data => %s", news_data["news_contents"][news_i])
        break


def test_news_content_to_json_file():
    news_data = business.get_news(3)
    with open("tests/samples/business_samples.json", "w") as f:
        json.dump(news_data, f, indent=2)
