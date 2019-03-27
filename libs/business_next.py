from bs4 import BeautifulSoup
import time
import json
import requests
import hashlib
import logging


class BusinessNext:

    def __init__(self):
        self.url = "https://www.bnext.com.tw/articles"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.81 Safari/537.36",
            "accept": "ttext/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.session = requests.Session()

    def get_news(self, page=1):
        resp = self.session.get(self.url, headers=self.headers)
        resp.encoding = 'utf-8'
        logging.debug("Encoding - [%s]" % resp.encoding)

        news_contents = dict()

        # get title text
        soup = BeautifulSoup(resp.text, "lxml")
        page_meta = soup.find('meta', {'property': "og:site_name"})
        csrf_token = soup.find('meta', {'name': "csrf-token"})["content"]
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
            for page_i in range(2, page + 1):
                others_pages_news_data = self.__load_pages(
                    page_index=page_i,
                    token=csrf_token)
                news_contents.update(others_pages_news_data)

        news_data["news_contents"] = news_contents

        # handle encoding
        news_data = json.dumps(news_data)
        news_data = json.loads(news_data)

        return news_data

    def __load_pages(self, page_index, token=None):
        _load_page_api = "https://www.bnext.com.tw/articles"
        logging.debug("Load page -> %s" % _load_page_api)

        payload = {
            "ac": "get_page",
            "offset": 8 + ((page_index - 1) * 12),
            "get_page_num": page_index,
            "page_sel": "#page_{}_".format(page_index),
            "type": "",
            "btn_sel": ".more_btn",
            "_token": token
        }

        load_resp = self.session.post(
            url=_load_page_api,
            data=payload)

        logging.debug("Load page status [%s]" % load_resp.status_code)
        if load_resp.status_code == 200:
            resp_data = load_resp.text
            raw_data = BeautifulSoup(resp_data, "lxml")
            text_content = raw_data.find("content").text
        else:
            raise Exception("Load page error")

        resp_data_dict = self.__handle_page_contents(data_contents=text_content)
        return resp_data_dict

    def __handle_page_contents(self, data_contents):
        data_soup = BeautifulSoup(data_contents, "lxml")

        # generate data dict
        _contents = dict()
        for tag_div in data_soup.findAll("div", {"class": "item_box item_sty01 div_tab"}):
            tag_a_img = tag_div.find("a", {"class": "item_img bg_img_sty01"})
            tag_div_title = tag_div.find("div", {"class": "item_title font_sty02"})
            news_link = tag_a_img["href"]
            news_title = tag_div_title.text.strip()
            img_link = tag_a_img.find("img")["src"]
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

    tech_news = BusinessNext()
    news_data = tech_news.get_news(10)
    print(news_data)
    print("Get tech news data counts -> %s" % len(news_data["news_contents"]))
