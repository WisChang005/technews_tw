from libs.ithome import ITHOME
from libs.tech_orange import TechOrange
from libs.business_next import BusinessNext
import pytest
import logging


strFormat = '%(asctime)s [%(module)s.%(funcName)s]' \
    ' %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=strFormat)

ithome = ITHOME()
tech_orange = TechOrange()
business_next = BusinessNext()
MORE_PAGE_TEST_INDEX = 5


@pytest.mark.incremental
class TechNewTests:

    @pytest.mark.parametrize("browser_page", [0, 1, 3, 5])
    def test_tech_orange_page_response(self, browser_page):
        news_data = tech_orange.get_news(browser_page)
        self.__news_data_contents_assertion(news_data)

    def test_tech_orange_page_load_verification(self):
        page1_data = tech_orange.get_news()
        page_more_data = tech_orange.get_news(MORE_PAGE_TEST_INDEX)
        self.__page_load_assertion(page1_data, page_more_data)

    @pytest.mark.parametrize("browser_page", [0, 1, 3, 5])
    def test_ithome_page_response(self, browser_page):
        news_data = ithome.get_news(browser_page)
        self.__news_data_contents_assertion(news_data)

    def test_ithome_page_load_verification(self):
        page1_data = ithome.get_news()
        page_more_data = ithome.get_news(MORE_PAGE_TEST_INDEX)
        self.__page_load_assertion(page1_data, page_more_data)

    @pytest.mark.parametrize("browser_page", [1, 3, 5])
    def test_business_next_page_response(self, browser_page):
        news_data = business_next.get_news(browser_page)
        self.__news_data_contents_assertion(news_data)

    def test_business_next_page_load_verification(self):
        page1_data = business_next.get_news()
        page_more_data = business_next.get_news(MORE_PAGE_TEST_INDEX)
        self.__page_load_assertion(page1_data, page_more_data)

    def __news_data_contents_assertion(self, news_data):
        assert "timestamp" in news_data
        assert "news_page_title" in news_data
        assert "news_contents" in news_data
        assert len(news_data["news_contents"]) > 0

    def __page_load_assertion(self, page1, page_more):
        assert len(page1["news_contents"]) < len(page_more["news_contents"])
