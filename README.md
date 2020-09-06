# Taiwan 科技新聞統整

![Tech News Watcher](https://github.com/WisChang005/technews_tw/workflows/Tech%20News%20Watcher/badge.svg)
[![codecov](https://codecov.io/gh/WisChang005/technews_tw/branch/master/graph/badge.svg)](https://codecov.io/gh/WisChang005/technews_tw)


## Why?
為了解決，需要訂閱許多科技新聞網站而生，整理每日科技新聞，定時派送e-mail給自己。


## Tech News Providers
```text
- iThome
- Tech Orange 科技報橘
- Business Next - 數位時代
- INSIDE 硬塞的
```

## Requirements
```bash
pip install technews-tw
```

## Get Today's News

取得今日新聞
```python
from technews import TechNews

TechNews("business").get_today_news()
TechNews("orange").get_today_news()
TechNews("ithome").get_today_news()
TechNews("inside").get_today_news()
```

## Get news by page

取得第1頁至第3頁所有科技新聞
```python
from technews import TechNews

TechNews("business").get_news_by_page(3)
TechNews("orange").get_news_by_page(3)
TechNews("ithome").get_news_by_page(3)
TechNews("inside").get_news_by_page(3)
```

## Send Today's News by Email

將今天的科技新聞傳送給接收者
```bash
# set environment variables
# sender only support "gmail" and "hotmail"
export MAIL_SENDER="sender@gmail.com"
export MAIL_SENDER_PWD="iampassword"
export MAIL_RECV="user01@gmail.com,user02@hotmail.com"

python -m technews.daily_news
```

## Integrate with Crontab

使用crontab，自動發送每日科技新聞，將下列指定寫入crontab設定檔
輸入: `crontab -e` 進入到設定介面
```shell
MAIL_SENDER="sender@gmail.com"
MAIL_SENDER_PWD="mypassword"
MAIL_RECV="receiver@gmail.com"
LOG_LEVEL="DEBUG"

# 每天晚上七點發送
0 19 * * 1-7 python3 -m technews.daily_news > technews_log.log 2>&1
```
