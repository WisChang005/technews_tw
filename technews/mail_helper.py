import copy
import random


class EmailContentHelper:

    NEWS_OUTLINE = """
      <!doctype html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>{email_title}</title>
        <link href="https://fonts.googleapis.com/css?family=Montserrat:200,300,400,500,600,700,800" rel="stylesheet">
      </head>
      <body style="padding: 0px; margin: 0px;font-family: 'Montserrat', sans-serif;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td align="center">
              <table width="600" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center">
                    <h2 style="letter-spacing: 0.2px; color: #3b95d1; text-transform: uppercase; font-weight: 700;
                      line-height: 20px; font-size: 24px;margin:37px 0;">{email_title}</h2>
                    <table align="center" width="520" border="0" cellspacing="0" cellpadding="3">
                      <!--/// New Data Row -->
                      {news_rows}
                      <!-- New Data Row ///-->
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
      </html>
    """

    IMG_TAG = """
        <td width="240">
            <a href="{news_link}">
                <img src="{img_link}" style="display: block; height:200px; width:240px;">
            </a>
        </td>
    """

    NEWS_TAG = """
        <td width="240">
            <h3 style="text-align:center; color:#250910; margin-bottom:16px;">{news_title}</h3>
            <p style="letter-spacing: 0.2px; color: #231f20; font-weight: 500;
                line-height: 20px; font-size: 16px;">{news_descrip}</p>
            <table width="240" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td width="0" valign="bottom"></td>
                <td width="240" valign="bottom" align="right">
                <a href="{news_link}" style="font-size: 14px; background: #3b95d1;
                    text-decoration: none; display: inline-block; text-align: center;
                    vertical-align: middle;line-height: 20px;padding: 10px 70px;
                    color:#fff;font-weight:500;margin-bottom: 40px;">VIEW MORE &raquo;
                </a>
                </td>
            </tr>
            </table>
        </td>
    """

    NEWS_ROW_DATA_PAIR = """
        <tr>
            <!-- Left Img ///-->
            {left_img_tag}
            <!--/// Left Img -->
            <td width="40"></td>
            <!-- Right Img ///-->
            {right_img_tag}
            <!--/// Right Img -->
        </tr>
        <tr>
            <!-- Left Data ///-->
            {left_news_data}
            <!--/// Left Data -->
            <td width="40"></td>
            <!-- Right Data ///-->
            {right_news_data}
            <!--/// Right Data -->
        </tr>
    """

    NEWS_ROW_DATA_ODD = """
        <tr>
            <!-- Left Img ///-->
            {left_img_tag}
            <!--/// Left Img -->
            <td width="40"></td>
        </tr>
        <tr>
            <!-- Left Data ///-->
            {left_news_data}
            <!--/// Left Data -->
            <td width="40"></td>
        </tr>
    """

    NEWS_PROVIDER_FRAME = """
        <tr>
            <td align="center" colspan="3">
                <h3 style="text-align:center; letter-spacing: 0.2px; color:#e65c00; text-transform: uppercase;
                    font-weight: 750; line-height: 20px; font-size: 26px;margin:37px 0;">{provider}
                </h3>
            </td>
        </tr>
    """

    def __init__(self):
        pass

    def get_news_html_contents(self, news_data, descrip=""):
        """
        news_data (dict):
            {
                "timestamp": 1553613896.8034308,
                "news_page_title": "iThome"
                "news_contents": {
                    "2a1bf0cedf6d8d855b432d1af5034f17": {
                    "link": "https://www.ithome.com.tw/news/129580",
                    "image": "https://s4.itho.me/sites/default/files/styles/picture...",
                    "title": "MIT用胺基酸序列搭配機器學習預測複雜蛋白質結構"
                    },
                    "deca65bdc81d9292541a47eaa435e9ce": {
                    "link": "https://www.ithome.com.tw/news/129594",
                    "image": "https://s4.itho.me/sites/default/files/styles/p...",
                    "title": "Google加碼投資臺灣，明年啟用臺灣新辦公室，可容納超過4千人"
                    },
                },
                ...
                ...
                ...
            }
        """
        news_html = ""
        news_html += self._get_news_provider_frame(news_data["news_page_title"])

        news_data_cp = copy.deepcopy(news_data)
        all_news = news_data_cp["news_contents"]
        while all_news:
            if (len(all_news) % 2) == 0:
                news1_key = random.choice(list(all_news.keys()))
                news1 = all_news[news1_key]
                news1_tag = self._get_news_tag(news1["title"], descrip, news1["link"])
                news1_img_tag = self._get_image_tag(news1["link"], news1["image"])
                all_news.pop(news1_key)

                news2_key = random.choice(list(all_news.keys()))
                news2 = all_news[news2_key]
                news2_tag = self._get_news_tag(news2["title"], descrip, news2["link"])
                news2_img_tag = self._get_image_tag(news2["link"], news2["image"])
                news_frame = self._get_news_row_pair_frame(news1_tag, news1_img_tag, news2_tag, news2_img_tag)
                all_news.pop(news2_key)
            else:
                news1_key = random.choice(list(all_news.keys()))
                news1 = all_news[news1_key]
                news1_tag = self._get_news_tag(news1["title"], "", news1["link"])
                news1_img_tag = self._get_image_tag(news1["link"], news1["image"])
                news_frame = self._get_news_row_frame(news1_tag, news1_img_tag)
                all_news.pop(news1_key)

            news_html += news_frame
        return news_html

    def get_email_html(self, title: str, news_rows: str):
        return self.NEWS_OUTLINE.format(email_title=title, news_rows=news_rows)

    def _get_news_provider_frame(self, news_provider: str):
        return self.NEWS_PROVIDER_FRAME.format(provider=news_provider)

    def _get_news_tag(self, descrip: str, title: str, link: str):
        return self.NEWS_TAG.format(news_title=title, news_descrip=descrip, news_link=link)

    def _get_image_tag(self, news: str, img: str):
        return self.IMG_TAG.format(news_link=news, img_link=img)

    def _get_news_row_pair_frame(self, link1: str, img1: str, link2: str, img2: str):
        return self.NEWS_ROW_DATA_PAIR.format(
            left_img_tag=img1, right_img_tag=img2, left_news_data=link1, right_news_data=link2)

    def _get_news_row_frame(self, link1: str, img1: str):
        return self.NEWS_ROW_DATA_ODD.format(left_img_tag=img1, left_news_data=link1)
