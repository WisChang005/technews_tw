import time
import json
import hashlib
import logging

import requests
from bs4 import BeautifulSoup


class Inside:

    def __init__(self):
        self.url = "https://www.inside.com.tw"
        self.headers = {
            "user-agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/85.0.4183.83 Safari/537.36")
        }
        self.session = requests.Session()

    def get_news(self, page=0):
        resp = self.session.get(self.url, headers=self.headers)
        logging.debug("Encoding - [%s]", resp.encoding)

        news_contents = dict()

        # get title text
        soup = BeautifulSoup(resp.text, "html5lib")
        page_meta = soup.find("title")
        page_title = page_meta.text.split("-")[0].strip()
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
        _load_page_api = "{}/?page={}"
        _load_page_api = _load_page_api.format(self.url, page_index)
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
        for tag_p in data_soup.find_all("div", {"class": "post_list_item"}):
            img_tag = tag_p.find("div", {"class": "post_cover_inner"})["style"]
            img_link = img_tag.split("url(")[1].strip(");").strip("'")
            tag_a_title = tag_p.find("a", {"class": "post_cover"})
            news_link = tag_a_title["href"]
            tag_p_title = tag_p.find("p", {"class": "post_description js-auto_break_text"})
            news_title = tag_p_title.text
            date_tag = tag_p.find("li", {"class": "post_date"})
            if date_tag:
                date = date_tag.span.text.strip().replace("/", "-")
            else:
                continue

            news_md5 = hashlib.md5(news_link.encode("utf-8")).hexdigest()
            cur_news_data = {
                news_md5: {
                    "link": news_link,
                    "image": img_link,
                    "title": news_title,
                    "date": date
                }
            }
            _contents.update(cur_news_data)
        return _contents
