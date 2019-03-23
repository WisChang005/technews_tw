from bs4 import BeautifulSoup
import time
import json
import requests
import datetime
import hashlib
import logging


class TechOrange:

    def __init__(self):
        self.url = "https://buzzorange.com/techorange/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.81 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.current_date = datetime.date.today().strftime("%Y/%m/%d")
        self.session = requests.Session()

    def get_news(self, page=1):
        resp = self.session.get(self.url, headers=self.headers)
        resp.encoding = 'utf-8'
        logging.debug("Encoding - [%s]" % resp.encoding)

        news_contents = dict()

        # get title text
        soup = BeautifulSoup(resp.text, "lxml")
        page_meta = soup.find("meta", {"name": "description"})
        page_title = page_meta["content"].strip()
        news_data = {
            "timestamp": time.time(),
            "news_page_title": page_title
        }
        logging.debug("Get tech news -> [%s]" % news_data)

        # get news data
        cur_news_data = self.__handle_page_contents(data_contents=resp.text)
        news_contents.update(cur_news_data)

        # get other pages
        if page >= 2:
            for page_i in range(2, page):
                others_pages_news_data = self.__load_pages(page_index=page_i)
                news_contents.update(others_pages_news_data)

        news_data["news_contents"] = news_contents
        logging.debug("Get tech news data -> %s" % len(news_data["news_contents"]))

        # handle encoding
        news_data = json.dumps(news_data)
        news_data = json.loads(news_data)

        return news_data

    def __load_pages(self, page_index):
        _load_page_api = "https://buzzorange.com/techorange/wp-admin/admin-ajax.php"
        _payload = {
            "action": "fm_ajax_load_more",
            "nonce": "fc7e9eb0b5",
            "page": page_index
        }

        load_resp = self.session.post(
            url=_load_page_api,
            data=_payload)

        logging.debug("Load page status [%s]" % load_resp.status_code)
        if load_resp.status_code == 200:
            resp_json = load_resp.json()
            resp_data = resp_json["data"]
        else:
            raise Exception("Load page error")

        resp_data_dict = self.__handle_page_contents(data_contents=resp_data)
        return resp_data_dict

    def __handle_page_contents(self, data_contents):
        data_soup = BeautifulSoup(data_contents, "lxml")

        # generate data dict
        _contents = dict()
        for tag_a in data_soup.findAll("a", {"class": "post-thumbnail"}):
            news_link = tag_a["href"]
            img_link = tag_a["style"].split(":url(")[1].strip(")")
            news_title1 = tag_a["onclick"].split("'Click', '")[1]
            news_title = news_title1.split("', {'nonInteraction'")[0]
            news_md5 = hashlib.md5(news_link.encode("utf-8")).hexdigest()
            cur_news_data = {
                news_md5: {
                    "link": news_link,
                    "image": img_link,
                    "title": news_title
                }
            }
            _contents.update(cur_news_data)

        return _contents


if __name__ == '__main__':

    strFormat = '%(asctime)s [%(module)s.%(funcName)s]' \
        ' %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=strFormat)

    tech_news = TechOrange()
    news_data = tech_news.get_news(page=1)
    print(news_data)
