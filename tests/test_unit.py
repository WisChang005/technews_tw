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


@pytest.mark.incremental
class TechNewTests:

    @pytest.mark.parametrize("browser_page", [0, 1, 3, 5])
    def test_tech_orange_page_response(self, browser_page):
        news_data = tech_orange.get_news(browser_page)
        self.__news_data_contents_assertion(news_data)

    def test_tech_orange_page_load_verification(self):
        page1_data = tech_orange.get_news()
        page10_data = tech_orange.get_news(10)
        self.__page_load_assertion(page1_data, page10_data)

    @pytest.mark.parametrize("browser_page", [0, 1, 3, 5])
    def test_ithome_page_response(self, browser_page):
        news_data = ithome.get_news(browser_page)
        self.__news_data_contents_assertion(news_data)

    def test_ithome_page_load_verification(self):
        page1_data = ithome.get_news()
        page10_data = ithome.get_news(10)
        self.__page_load_assertion(page1_data, page10_data)

    @pytest.mark.parametrize("browser_page", [0, 1, 3, 5])
    def test_business_next_page_response(self, browser_page):
        news_data = business_next.get_news(browser_page)
        self.__news_data_contents_assertion(news_data)

    def test_business_next_page_load_verification(self):
        page1_data = business_next.get_news()
        page10_data = business_next.get_news(10)
        self.__page_load_assertion(page1_data, page10_data)

    def __news_data_contents_assertion(self, news_data):
        assert "timestamp" in news_data
        assert "news_page_title" in news_data
        assert "news_contents" in news_data
        assert len(news_data["news_contents"]) > 0

    def __page_load_assertion(self, page1, page10):
        assert len(page1["news_contents"]) < len(page10["news_contents"])
