import time
import hashlib
import logging

import time
import requests


class BusinessNext:

    def __init__(self):
        self.timestamp = time.time()
        self.url = f"https://www.bnext.com.tw/api/article/list?" \
            f"timestamp={self.timestamp}&sign=T2cUU8eV5IDGguY1BdESrmxRUHGYbqDicD02K8ixZZI%253D"
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

    def get_news(self, page=1):
        resp = self.session.post(self.url, headers=self.headers, data={"page": page})
        news_contents = dict()

        # # get title text
        news_data = {
            "timestamp": time.time(),
            "news_page_title": "Business Next"
        }

        if page >= 2:
            for page_i in range(2, page + 1):
                others_pages_news_data = self.__load_pages(page_index=page_i)
                news_contents.update(others_pages_news_data)

        # # get news data
        cur_news_data = self.__handle_page_contents(data_contents=resp.json())
        news_contents.update(cur_news_data)
        news_data["news_contents"] = news_contents

        return news_data

    def __load_pages(self, page_index, token=None):

        load_resp = self.session.post(
            url=self.url,
            data={"page": page_index})

        logging.debug("Load page status [%s]", load_resp.status_code)
        resp_data_dict = self.__handle_page_contents(load_resp.json())
        return resp_data_dict

    def __handle_page_contents(self, data_contents):
        # generate data dict
        _contents = dict()
        for d in data_contents["data"]["data"]:
            post_date = d["shortDate2"].replace(".", "-")
            news_link = d["amp_link"]
            news_title = d["title"]
            img_link = d["medium"]
            news_md5 = hashlib.md5(news_link.encode("utf-8")).hexdigest()
            cur_news_data = {
                news_md5: {
                    "link": news_link,
                    "image": img_link,
                    "title": news_title,
                    "date": post_date}
            }
            _contents.update(cur_news_data)

        return _contents
