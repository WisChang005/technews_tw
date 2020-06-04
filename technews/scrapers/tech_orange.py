import time
import json
import hashlib
import logging

import requests
from bs4 import BeautifulSoup


class TechOrange:

    def __init__(self):
        self.url = "https://buzzorange.com/techorange/"
        self.headers = {
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/58.0.3029.81 Safari/537.36"),
            "accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                       "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"),
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "upgrade-insecure-requests": "1"
        }
        self.session = requests.Session()

    def get_news(self, page=1):
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
                    "news_page_title": soup.find("title").text.strip()
                }

                # get load page key
                load_more_key = None
                script_tags = soup.findAll("script", {"type": "text/javascript"})
                for _, js_script in enumerate(script_tags):
                    if "fmloadmore" in js_script.text:
                        split_string = str(js_script.text.split("fmloadmore = ")[1].split(";")[0])
                        logging.debug("@@@ split_string = %s", split_string)
                        _split_dict = json.loads(split_string)
                        logging.debug("@@@ _split_dict = %s", _split_dict)
                        load_more_key = _split_dict["nonce"]
                        break

                if not load_more_key:
                    raise Exception(f"Get load page key error {load_more_key}")

                logging.debug("Load page key -> [%s]", load_more_key)
                break

            except Exception as e:
                logging.warning("The key is wrong, wait 5 sec do retry...%s", e)
                time.sleep(5)
                self.session = requests.Session()
        else:
            raise ValueError(f"Loading key error {load_more_key}")

        # get news data
        cur_news_data = self.__handle_page_contents(data_contents=resp.text)
        news_contents.update(cur_news_data)

        # get other pages
        if page >= 2:
            for page_i in range(2, page + 1):
                others_pages_news_data = self.__load_pages(
                    page_index=page_i, nonce_key=load_more_key)
                news_contents.update(others_pages_news_data)

        news_data["news_contents"] = news_contents

        return json.loads(json.dumps(news_data))

    def __load_pages(self, page_index, nonce_key):
        _load_page_api = "https://buzzorange.com/techorange/wp-admin/admin-ajax.php"
        _payload = {
            "action": "fm_ajax_load_more",
            "nonce": nonce_key,
            "page": page_index
        }

        load_resp = self.session.post(
            url=_load_page_api,
            data=_payload)

        logging.debug("Load page status [%s]", load_resp.status_code)
        retry_counts = 0
        while load_resp.status_code != 200:
            load_resp = self.session.post(
                url=_load_page_api,
                data=_payload)
            logging.debug("[RETRY] Load page status [%s]", load_resp.status_code)

            if retry_counts > 3:
                raise Exception("load page error")

            retry_counts += 1
            time.sleep(5)

        resp_json = load_resp.json()
        resp_data = resp_json["data"]

        resp_data_dict = self.__handle_page_contents(data_contents=resp_data)
        return resp_data_dict

    def __handle_page_contents(self, data_contents):
        data_soup = BeautifulSoup(data_contents, "lxml")

        # generate data dict
        _contents = dict()

        for article_i in data_soup.find_all("article"):
            tag_a = article_i.find("a", {"class": "post-thumbnail"})
            news_link = tag_a["href"]
            img_link = tag_a["data-src"].strip()
            news_title1 = tag_a["onclick"].split("'Click', '")[1]
            news_title = news_title1.split("', {'nonInteraction'")[0]
            news_md5 = hashlib.md5(news_link.encode("utf-8")).hexdigest()
            date = article_i.find("time").text.replace("/", "-")
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
