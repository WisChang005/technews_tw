import time
import json
import hashlib
import logging

import requests
from bs4 import BeautifulSoup


class TechOrange:

    def __init__(self):
        self.url = "https://buzzorange.com/techorange/latest/"
        self.headers = {
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/58.0.3029.81 Safari/537.36"),
            "accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                       "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"),
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1"
        }
        self.session = requests.Session()

    def get_news(self, page=1):
        load_more_key = None
        for _ in range(3):
            try:
                resp = self.session.get(self.url, headers=self.headers)
                resp.encoding = 'utf-8'
                logging.debug("Encoding - [%s]", resp.encoding)

                news_contents = dict()

                # get title text
                soup = BeautifulSoup(resp.text, "html5lib")
                news_data = {
                    "timestamp": time.time(),
                    "news_page_title": soup.find("title").text.split("|")[1].strip()
                }
                data_soup = BeautifulSoup(resp.text, "lxml")
                break

            except Exception as e:
                logging.warning("The key is wrong, wait 5 sec do retry...%s", e)
                time.sleep(5)
                self.session = requests.Session()
        else:
            raise ValueError(f"Loading key error {load_more_key}")

        # get news data
        cur_news_data = self.__handle_page_contents(data_soup)
        news_contents.update(cur_news_data)

        news_data["news_contents"] = news_contents

        return json.loads(json.dumps(news_data))

    def __load_pages(self, page_index, nonce_key):
        _load_page_api = "https://buzzorange.com/techorange/wp/wp-admin/admin-ajax.php"
        _payload = {
            "postOffset": (page_index * 8),
            "type": "loadmore"
        }
        _payload.update(nonce_key)

        logging.debug(_payload)
        self.session.headers.update({
            "x-requested-with": "XMLHttpRequest",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        })
        load_resp = self.session.post(
            url=_load_page_api,
            data=json.dumps(_payload))

        logging.debug("Load page status [%s]", load_resp.status_code)
        logging.debug("content: [%s]", load_resp.content)

        resp_data = load_resp.text
        print(resp_data)

        resp_data_dict = self.__handle_page_contents(resp_data)
        return resp_data_dict

    def __handle_page_contents(self, data_soup):

        # generate data dict
        _contents = dict()

        for article_i in data_soup.find_all("div", {"class": "col-md-6 col-sm-6 list-item"}):
            tag_a = article_i.find("a")
            news_link = tag_a["href"]
            img_link = tag_a.find("img")["src"]
            news_title = article_i.find("h3", {"class": "post__title typescale-2"}).a.text
            news_md5 = hashlib.md5(news_link.encode("utf-8")).hexdigest()
            date = article_i.find("time").text.replace("/", "-")
            logging.debug(f"news_link={news_link}, img_link={img_link}, news_title={news_title}, date={date}")
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

    def _get_load_page_args(self, data_soup):
        scripts = data_soup.find("script", {"id": "ceris-scripts-js-extra"})
        args_json = json.loads(scripts.string.split('ajax_buff = ')[1].split(';')[0])
        logging.debug(f"scripts -> {json.dumps(args_json, indent=2)}")
        args_data = args_json["query"]["ceris_posts_listing_grid-613c1cb3a98c1"]
        security_code = args_json["ceris_security"]["ceris_security_code"]["content"]
        data = {}
        data.update(args_data)
        data.update({"action": "ceris_posts_listing_grid"})
        data.update({"securityCheck": security_code})
        logging.debug(f"data -> {data}")
        return data
