# Taiwan Tech News Parser - 科技新聞

![Tech News Watcher](https://github.com/WisChang005/technews_tw/workflows/Tech%20News%20Watcher/badge.svg)
[![codecov](https://codecov.io/gh/WisChang005/technews_tw/branch/master/graph/badge.svg)](https://codecov.io/gh/WisChang005/technews_tw)


##### 台灣科技新聞
```
Support sites:
    - iThome
    - Tech Orange 科技報橘
    - Business Next - 數位時代
```

##### Package Requirements
```
pip install -r requirements.txt
```

##### Example for iThome:
```
from technews.ithome import ITHOME

tech_news = ITHOME()

# get page 1 news
news_data = tech_news.get_news()

# get news from page 1 - 10
news_data = tech_news.get_news(10)

# get todays news
news_data = tech_news.get_today_news(10)
```

##### Return Samples:
```
{
  "timestamp": 1590426096.36479,
  "news_page_title": "TechOrange",
  "news_contents": {
    "355de9fb470db9abe536e4c5fb47b87f": {
      "link": "https://buzzorange.com/techorange/2020/05/25/digital-transformation-strategy/",
      "image": "https://buzzorange.com/techorange/wp-content/uploads/sites/2/2020/05/\u4f01\u696d\u6578\u4f4d\u8f49\u578b.webp?jpg",
      "title": "\u7cbe\u6e96\u6295\u5165\u6578\u4f4d\u8f49\u578b\u5fc5\u8981\u8cc7\u6e90\uff01\u4f01\u696d\u5982\u4f55\u5efa\u69cb\u6700\u4f73\u7b56\u7565\uff1f",
      "date": "2020-05-25"
    },
    "cc19e14e400065d9b9e47afcd0415d78": {
      "link": "https://buzzorange.com/techorange/2020/05/21/cloudmile-ai/",
      "image": "https://buzzorange.com/techorange/wp-content/uploads/sites/2/2020/05/Ainotam-5146.webp?jpg",
      "title": "\u3010\u884c\u92b7\u4eba\u5225\u518d\u50bb\u50bb\u52a0\u73ed\u3011\u5ee3\u544a\u696d AI \u8f49\u578b\u5be6\u6230\u7d93\u9a57\uff1a\u6bcf\u4eba\u4e00\u5929\u7701\u4e0b 1.5 \u5c0f\u6642\uff01",
      "date": "2020-05-21"
    },
    ...
  }
}
```


### To Do
------------
[Tech News - 科技新報](https://technews.tw/)

[INSIDE 硬塞的](https://www.inside.com.tw/)

