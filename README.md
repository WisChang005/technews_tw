# 科技新聞 8拉888!

![Tech News Watcher](https://github.com/WisChang005/technews_tw/workflows/Tech%20News%20Watcher/badge.svg)
[![codecov](https://codecov.io/gh/WisChang005/technews_tw/branch/master/graph/badge.svg)](https://codecov.io/gh/WisChang005/technews_tw)

![news intor](imgs/intor.png)

## Supported News
```
- iThome
- Tech Orange 科技報橘
- Business Next - 數位時代
```

## Package Requirements
```
# Install requirements only
pip install -r requirements.txt

or

# Install to site-packages
pip install -e technews_tw
```

## Get Today's News:
```python
from technews import TechNews


TechNews("business").get_today_news()
TechNews("orange").get_today_news()
TechNews("ithome").get_today_news()
```

## Send Today's News by Email
```python

from technews import mail_util
from technews import TechNews
from technews import EmailContentHelper


# get news from page 1 to 3
news = TechNews("orange").get_news_by_page(3)

# create email html 
mh = EmailContentHelper()
news_contents = mh.get_news_html_contents(news, news["news_page_title"])
news_html = mh.get_email_html("Test-科技新聞", news_rows)

# send mail
mail_util.mail_sender(
        mail_sender, mail_sender_pwd,
        recv_mails, news_html, "Test-科技新聞", "html")
```


### To Do
------------
[Tech News - 科技新報](https://technews.tw/)

[INSIDE 硬塞的](https://www.inside.com.tw/)

