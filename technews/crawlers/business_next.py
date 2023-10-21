import time
import hashlib
import logging

import time
import requests
from bs4 import BeautifulSoup


class BusinessNext:

    def __init__(self):
        self.timestamp = time.time()
        self.url = f"https://www.bnext.com.tw/articles"
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
        params = {
            "page": page,
        }
        resp = self.session.get(self.url, headers=self.headers, params=params)
        news_contents = dict()

        # # get title text
        news_data = {
            "timestamp": time.time(),
            "news_page_title": "Business Next"
        }

        if resp.status_code == 200:
            resp_data = resp.text
        else:
            raise Exception("Load page error")

        # # get news data
        cur_news_data = self.__handle_page_contents(data_contents=resp_data)
        news_contents.update(cur_news_data)
        news_data["news_contents"] = news_contents

        return news_data

    def __handle_page_contents(self, data_contents):
        data_soup = BeautifulSoup(data_contents, "lxml")

        # generate data dict
        _contents = dict()
        for d in data_soup.find_all("div", {"class": "flex flex-col gap-3 relative h-full"}):
            date_div = d.find("div", {"class":"flex relative items-center gap-2 text-xs text-gray-500 font-normal"})
            post_date = ""
            for date_span in date_div.find_all("span"):
                if "|" not in date_span.text:
                    post_date = date_span.text
                    break
            news_link = d.find("a", {"class": "absolute inset-0"})["href"]
            news_title = d.find("h2", {"class": "text-lg"}).text
            img_link =d.find("img", {"class": "aspect-[16/9] object-cover rounded-none"})["src"]
            news_md5 = hashlib.md5(news_link.encode("utf-8")).hexdigest()

            cur_news_data = {
                news_md5: {
                    "link": news_link,
                    "image": img_link,
                    "title": news_title,
                    "date": post_date
                }
            }
            _contents.update(cur_news_data)

        return _contents
