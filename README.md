# 科技新聞 8拉888!

![Tech News Watcher](https://github.com/WisChang005/technews_tw/workflows/Tech%20News%20Watcher/badge.svg)
[![codecov](https://codecov.io/gh/WisChang005/technews_tw/branch/master/graph/badge.svg)](https://codecov.io/gh/WisChang005/technews_tw)

![news intor](imgs/intor.png)

## Supported News
```
- iThome
- Tech Orange 科技報橘
- Business Next - 數位時代
- INSIDE 硬塞的
```

## Package Requirements
```
# Install requirements only
pip install -r requirements.txt

or

# Install to site-packages
git clone https://github.com/WisChang005/technews_tw.git

pip install -e technews_tw
```

## Get Today's News:
```python
from technews import TechNews


TechNews("business").get_today_news()
TechNews("orange").get_today_news()
TechNews("ithome").get_today_news()
TechNews("inside").get_today_news()
```

## Send Today's News by Email

#### Linux
```bash
# set environment variables
# sender only support "gmail" and "hotmail"
export MAIL_SENDER="sender@gmail.com"
export MAIL_SENDER_PWD="iampassword"
export MAIL_RECV="user01@gmail.com,user02@hotmail.com"

python -m technews.daily_news
```

### To Do
------------
[Tech News - 科技新報](https://technews.tw/)
