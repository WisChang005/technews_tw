import time
import json
import hashlib
import logging

import requests
from bs4 import BeautifulSoup


class iThome:

    def __init__(self):
        self.url = "https://www.ithome.com.tw/latest"
        self.headers = {
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/58.0.3029.81 Safari/537.36"),
            "accept": ("ttext/html,application/xhtml+xml,application/xml;"
                       "q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"),
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.session = requests.Session()

    def get_news(self, page=0):
        resp = self.session.get(self.url, headers=self.headers)
        resp.encoding = 'utf-8'
        logging.debug("Encoding - [%s]", resp.encoding)

        news_contents = dict()

        # get title text
        soup = BeautifulSoup(resp.text, "html5lib")
        page_meta = soup.find('meta', {'property': "og:site_name"})
        page_title = page_meta["content"].strip()
        news_data = {
            "timestamp": time.time(),
            "news_page_title": page_title
        }
        logging.debug("Get tech news -> [%s]", news_data)

        # get news data
        cur_news_data = self.__handle_page_contents(data_contents=resp.text)
        news_contents.update(cur_news_data)

        # get other pages
        if page >= 1:
            for page_i in range(1, page + 1):
                others_pages_news_data = self.__load_pages(page_index=page_i)
                news_contents.update(others_pages_news_data)

        news_data["news_contents"] = news_contents

        # handle encoding
        news_data = json.dumps(news_data)
        news_data = json.loads(news_data)

        return news_data

    def __load_pages(self, page_index):
        _load_page_api = "https://www.ithome.com.tw/latest?page={}"
        _load_page_api = _load_page_api.format(page_index)
        load_resp = self.session.get(url=_load_page_api)

        if load_resp.status_code == 200:
            resp_data = load_resp.text
        else:
            raise Exception("Load page error")

        resp_data_dict = self.__handle_page_contents(data_contents=resp_data)
        return resp_data_dict

    def __handle_page_contents(self, data_contents):
        data_soup = BeautifulSoup(data_contents, "lxml")

        # generate data dict
        _base_url = "https://www.ithome.com.tw"
        _contents = dict()
        for tag_p in data_soup.find_all("div", {"class": "views-field views-field-created"}):
            tag_p_title = tag_p.find("p", {"class": "title"})
            tag_p_img = tag_p.find("p", {"class", "photo"})
            tag_a_title = tag_p_title.find("a")
            tag_a_img = tag_p_img.find("a")
            news_link = tag_a_title["href"]
            news_title = tag_a_title.text
            date = tag_p.find("p", {"class": "post-at"}).text.strip()
            try:
                img_link = tag_a_img.find("img")["src"]
            except Exception:
                img_link = None
            news_md5 = hashlib.md5(news_link.encode("utf-8")).hexdigest()
            cur_news_data = {
                news_md5: {
                    "link": _base_url + news_link,
                    "image": img_link,
                    "title": news_title,
                    "date": date
                }
            }
            _contents.update(cur_news_data)

        return _contents
