# Taiwan Tech News Parser - 科技新聞文章擷取

![Tech News Watcher](https://github.com/WisChang005/technews_tw/workflows/Tech%20News%20Watcher/badge.svg)
[![codecov](https://codecov.io/gh/WisChang005/technews_tw/branch/master/graph/badge.svg)](https://codecov.io/gh/WisChang005/technews_tw)


##### 台灣科技新聞
```
支援以下網站:
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

# get page 1 news
tech_news = ITHOME()
news_data = tech_news.get_news()

# get news from page 1 - 10
tech_news = ITHOME()
news_data = tech_news.get_news(10)
```

##### Return Samples:
```
{
  "timestamp": 1553613896.8034308,
  "news_page_title": "iThome"
  "news_contents": {
    "2a1bf0cedf6d8d855b432d1af5034f17": {
      "link": "https://www.ithome.com.tw/news/129580",
      "image": "https://s4.itho.me/sites/default/files/styles/picture_size_small/public/field/image/ying_mu_kuai_zhao_2019-03-25_xia_wu_12.59.27.png?itok=HWs33IWQ",
      "title": "MIT用胺基酸序列搭配機器學習預測複雜蛋白質結構"
    },
    "deca65bdc81d9292541a47eaa435e9ce": {
      "link": "https://www.ithome.com.tw/news/129594",
      "image": "https://s4.itho.me/sites/default/files/styles/picture_size_small/public/field/image/google2_she_ying_huang_yu_yun_.jpg?itok=86TCRP2X",
      "title": "Google加碼投資臺灣，明年啟用臺灣新辦公室，可容納超過4千人"
    },
  },
  ...
  ...
  ...
}
```


### To Do
------------
[Tech News - 科技新報](https://technews.tw/)

[INSIDE 硬塞的](https://www.inside.com.tw/)

