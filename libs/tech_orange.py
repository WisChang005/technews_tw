from bs4 import BeautifulSoup
import time
import json
import requests
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
        self.session = requests.Session()

    def get_news(self, page=1):
        for _ in range(3):
            try:
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

                # get load page key
                script_tags = soup.findAll("script", {"type": "text/javascript"})
                for i, js_script in enumerate(script_tags):
                    if "fmloadmore" in js_script.text:
                        logging.debug(js_script.text)
                        _split_dict = json.loads(str(js_script.text.split("fmloadmore = ")[1].split(";")[0]))
                        logging.debug(_split_dict)
                        load_more_key = _split_dict["nonce"]
                        logging.debug("Load more key [%s]" % load_more_key)
                        break

                try:
                    int(load_more_key)
                except ValueError:
                    logging.info("The key is correct!")
                else:
                    raise ValueError("The Key is wrong!")

            except Exception as e:
                logging.error(e)
                logging.warn("The key is wrong, wait 5 sec do retry...")
                time.sleep(5)
                self.session = requests.Session()

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

        # handle encoding
        news_data = json.dumps(news_data)
        news_data = json.loads(news_data)

        return news_data

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

        logging.debug("Load page status [%s]" % load_resp.status_code)
        retry_counts = 0
        while load_resp.status_code != 200:
            load_resp = self.session.post(
                url=_load_page_api,
                data=_payload)
            logging.debug("[RETRY] Load page status [%s]" % load_resp.status_code)

            if retry_counts > 3:
                raise Exception("load page error")

            retry_counts += 1
            time.sleep(5)
        else:
            resp_json = load_resp.json()
            resp_data = resp_json["data"]

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
    news_data = tech_news.get_news(page=3)
    print(news_data)
    print("Get tech news data counts -> %s" % len(news_data["news_contents"]))
