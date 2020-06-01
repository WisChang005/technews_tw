# Taiwan Tech News - 科技新聞

![Tech News Watcher](https://github.com/WisChang005/technews_tw/workflows/Tech%20News%20Watcher/badge.svg)
[![codecov](https://codecov.io/gh/WisChang005/technews_tw/branch/master/graph/badge.svg)](https://codecov.io/gh/WisChang005/technews_tw)


## Supported News
```
Support sites:
    - iThome
    - Tech Orange 科技報橘
    - Business Next - 數位時代
```

## Package Requirements
```
# Install requirements only
pip install -r requirements.txt

or

# Install to site-package
pip install -e technews_tw
```

## Get Today's News:
```
from technews import TechNews


TechNews("business").get_today_news()
TechNews("orange").get_today_news()
TechNews("ithome").get_today_news()
```


### To Do
------------
[Tech News - 科技新報](https://technews.tw/)

[INSIDE 硬塞的](https://www.inside.com.tw/)

