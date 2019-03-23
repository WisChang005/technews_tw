#! /usr/bin/python3
import sys
import os
import datetime
import requests
import logging as log
from bs4 import BeautifulSoup
from utils.emailUtil import EmailHtmlTemplate
from utils import utils
from utils.GoogleDriveUtil import GoogleDrive

CURRENT_DATE = datetime.date.today().strftime("%Y/%m/%d")
FILE_DATE = CURRENT_DATE.replace('/', '')
FILENAME = '%s/news_data_%s.txt' % (os.getcwd(), FILE_DATE)
NEWSFILE_ALL = '%s/news_data_*.txt' % os.getcwd()


def decorateNewsErH(func):

    def d_f(*args, **kargs):
        news_dict = dict()
        news_title = ''
        try:
            news_dict, news_title = func(*args, **kargs)
        except Exception:
            print('[ DEBUG ] Get News error')
            print(utils.getException())
        return news_dict, news_title

    return d_f


@decorateNewsErH
def get_techorange_news():
    print('[ DEBUG ] Get Tech Orange news')
    techorange_url = "https://buzzorange.com/techorange/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/58.0.3029.81 Safari/537.36'
    }
    dom = utils.get_web_page(url=techorange_url, header=headers)
    soup = BeautifulSoup(dom.text, 'lxml')

    # get picture
    img_dict = dict()
    for tag_a_img in soup.findAll('a', {'class': 'post-thumbnail'}):
        linkkey = tag_a_img['href']
        img_link = tag_a_img['style'].split(':url(')[1].strip(')')
        img_dict.update({linkkey: img_link})

    techorange_web_title = soup.find('meta', {"name": "description"})
    techorange_web_title = techorange_web_title['content'].strip()
    techorange_web_title = "[ {title} ]".format(title=techorange_web_title)

    tech_news_dict = dict()
    for tag_a in soup.findAll('a'):
        news_text = tag_a.text
        news_link = tag_a['href']
        # check link is already sent
        if (CURRENT_DATE in news_link) and (news_text.strip() is not ''):
            news_img = img_dict[news_link]
            news_text = '%s - %s' % (techorange_web_title, news_text)
            ck_st = is_in_newsfile(ck_link=news_link)
            if not ck_st:
                write_text_file(
                    _fpath=FILENAME, _write_mode='a', _text=news_link)
                tech_news_dict.update({news_text: [news_link, news_img]})

    return tech_news_dict, techorange_web_title


@decorateNewsErH
def get_ithome_news():
    print('[ DEBUG ] Get iThome news')
    ithome_url = "http://www.ithome.com.tw/latest"
    ithome_news_dict = dict()

    for page_index in range(3):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.81 Safari/537.36',
            'page': str(page_index)
        }
        dom = utils.get_web_page(url=ithome_url, header=headers)
        soup = BeautifulSoup(dom.text, 'lxml')

        photo_list = soup.findAll('p', {'class': 'photo'})
        photo_dict = dict()
        for photo_i in photo_list:
            imgkey = photo_i.find('a')
            if imgkey:
                imgkey = imgkey['href']
                imglink = photo_i.find('img')['src'].split('?')[0]
                photo_dict.update({imgkey: imglink})

        ithome_web_title = soup.find('meta', {'property': "og:site_name"})
        ithome_web_title_ori = ithome_web_title['content'].strip()
        ithome_web_title = "[ {title} ]".format(title=ithome_web_title_ori)

        category_list = soup.findAll('p', {'class': 'category'})
        title_list = soup.findAll('p', {'class': 'title'})
        postat_list = soup.findAll('p', {'class': 'post-at'})
        for i, date_p in enumerate(postat_list):
            if date_p.text.strip() == CURRENT_DATE.replace('/', '-'):
                news_text = title_list[i].text
                news_category_list = category_list[i].findAll('a')
                # if get category fail put news title
                try:
                    news_category = news_category_list[1].text
                except Exception:
                    news_category = ithome_web_title_ori

                news_text = '[ %s ] - %s' % (news_category, news_text)
                link_tail = title_list[i].find('a')['href']
                if link_tail not in photo_dict:
                    continue
                news_link = 'http://www.ithome.com.tw' + link_tail
                news_img = photo_dict[link_tail]

                # check link is already sent
                ck_st = is_in_newsfile(ck_link=news_link)
                if not ck_st:
                    write_text_file(
                        _fpath=FILENAME, _write_mode='a', _text=news_link)
                    ithome_news_dict.update({news_text: [news_link, news_img]})

    return ithome_news_dict, ithome_web_title


@decorateNewsErH
def get_bnext_news():
    print('[ DEBUG ] Get B.Next news')
    bnext_dict = dict()
    bnext_url = 'https://www.bnext.com.tw/articles'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/58.0.3029.81 Safari/537.36'
    }
    dom = utils.get_web_page(url=bnext_url, header=headers)
    soup = BeautifulSoup(dom.text, 'lxml')

    bnext_title = soup.find('meta', {'property': "og:site_name"})
    bnext_title = bnext_title['content'].strip()
    bnext_web_title = "[ {title} ]".format(title=bnext_title)

    div_list = soup.findAll('div', {'class': 'item_box item_sty01 div_tab '})

    date_list = list()
    category_list = list()
    for div_title in div_list:
        date_text = div_title.find('div', {'class': "div_td td1"}).text.strip()
        news_tag = div_title.find('div', {'class': 'item_tags'})
        try:
            news_category = news_tag.find('a').text
        except Exception:
            news_category = bnext_title
        category_list.append(news_category)
        date_list.append(date_text)

    date_index = 0
    img_dict = dict()
    for tag_a in soup.findAll('a'):
        if 'item_img bg_img_sty01' in str(tag_a):
            linkkey = tag_a['href']
            news_img = tag_a['style'].split(': url(\'')[1].split('?')[0]
            print(linkkey, news_img)
            img_dict.update({linkkey: news_img})

        if 'item_title font_sty02' in str(tag_a):
            news_link = tag_a['href']
            news_img = img_dict[news_link].replace('3x2', '2x1')
            find_class = {'class': 'item_title font_sty02'}
            news_text = tag_a.find('div', find_class).text.strip()
            if ('-' not in date_list[date_index]):
                string_tuple = (category_list[date_index], news_text)
                news_text = '[ %s ] - %s' % string_tuple
                # check link is already sent
                ck_st = is_in_newsfile(ck_link=news_link)
                if not ck_st:
                    write_text_file(
                        _fpath=FILENAME, _write_mode='a', _text=news_link)
                    bnext_dict.update({news_text: [news_link, news_img]})

            date_index += 1

    return bnext_dict, bnext_web_title


@decorateNewsErH
def get_inside_news():

    def get_article_img(news_url):
        rs = requests.session()
        dom = rs.get(news_url, verify=False)
        print('[Status code] %s' % dom.status_code)
        dom.encoding = 'utf-8'
        soup = BeautifulSoup(dom.text, 'lxml')
        post_class = {'class': 'post_content article'}
        img_link = soup.find('div',
                             post_class).find('img')['srcset'].split(' ')[2]
        return img_link

    print('[ DEBUG ] Get inside news')
    inside_dict = dict()
    inside_url = "https://www.inside.com.tw/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/58.0.3029.81 Safari/537.36'
    }

    dom = utils.get_web_page(url=inside_url, header=headers)
    soup = BeautifulSoup(dom.text, 'lxml')

    inside_title_ori = soup.find('title').text.split('-')[0].strip()
    inside_title = "[ {title} ]".format(title=inside_title_ori)

    for tag_div in soup.findAll('div', {'class': 'post_list_item'}):
        try:
            news_a = tag_div.find('a', {'class': 'js-auto_break_title'})
            news_text = news_a.text.strip()
            news_link = news_a['href'].strip()
            tag_a = tag_div.findAll('a', {'class': 'hero_slide_tag'})
            # if get category fail put in news title
            try:
                news_category = tag_a[1].text
            except Exception:
                news_category = inside_title_ori
            news_text = '[ %s ] - %s' % (news_category, news_text)

        except Exception:
            pass

        else:
            if CURRENT_DATE in news_link:
                # get news img link
                news_img = get_article_img(news_url=news_link)
                # check link is already sent
                ck_st = is_in_newsfile(ck_link=news_link)
                if not ck_st:
                    write_text_file(
                        _fpath=FILENAME, _write_mode='a', _text=news_link)
                    inside_dict.update({news_text: [news_link, news_img]})

    return inside_dict, inside_title


@decorateNewsErH
def get_tw_tech_news():
    print('[ DEBUG ] Get TWTech news')
    tech_news_dict = dict()
    sub_webframe = ["", "page/2/", "page/3/"]
    for sub_page in sub_webframe:
        tech_news_url = "https://technews.tw/" + sub_page
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.81 Safari/537.36'
        }

        dom = utils.get_web_page(url=tech_news_url, header=headers)
        soup = BeautifulSoup(dom.text, 'lxml')

        # get news picture
        img_dict = dict()
        for j, div_tag in enumerate(soup.findAll('div', {'class': 'img'})):
            try:
                newslink = div_tag.find('a')['href']
                imglink = div_tag.find('img')['src']

            except Exception:
                newslink = False

            if newslink:
                img_dict.update({newslink: imglink})

        technews_title = soup.find('meta', {'name': 'Title'})
        technews_title_ori = technews_title['content'].split('|')[0].strip()
        technews_title = "[ {title} ]".format(title=technews_title_ori)

        for tag_header in soup.findAll('header', {'class': 'entry-header'}):
            tag_h1 = tag_header.find('h1', {'class': 'entry-title'})
            span_class = {
                'class': 'body',
                'style': 'font-size: 12px;color: #6b6b6b;'
            }
            tag_span = tag_header.find('span', span_class)
            # if get category fail put news title
            try:
                news_category = tag_span.find('a').text
            except Exception:
                news_category = technews_title_ori

            tag_a = tag_h1.find('a')
            news_text = tag_a.text
            news_link = tag_a['href']
            news_img = img_dict[news_link]
            news_text = '[ %s ] - %s' % (news_category, news_text)
            if (CURRENT_DATE in news_link):
                # check link is already sent
                ck_st = is_in_newsfile(ck_link=news_link)
                if not ck_st:
                    write_text_file(
                        _fpath=FILENAME, _write_mode='a', _text=news_link)
                    tech_news_dict.update({news_text: [news_link, news_img]})

    return tech_news_dict, technews_title


@decorateNewsErH
def get_tech_crunch():
    print('[ DEBUG ] Get TechCrunch news')
    tech_news_dict = dict()
    sub_webframe = ["", "page/2/", "page/3/"]
    for sub_page in sub_webframe:
        tech_news_url = "http://techcrunch.cn/{page}".format(page=sub_page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.81 Safari/537.36'
        }

        dom = utils.get_web_page(url=tech_news_url, header=headers)
        soup = BeautifulSoup(dom.text, 'lxml')

        technews_title = soup.find('title').text.split('-')[0].strip()
        tech_crunch_title = "[ {title} ]".format(title=technews_title)
        print('Title: %s' % tech_crunch_title)

        for tag_li in soup.findAll('li', {'class': 'river-block'}):

            crunch_news_link = tag_li['data-permalink']
            crunch_news_text = tag_li['data-sharetitle']
            img_tag = tag_li.find('a', {'class': 'thumb'})
            crunch_news_text = '%s - %s' % (
                tech_crunch_title, crunch_news_text)
            # print('crunch_news_text = %s' % crunch_news_text)
            # print('crunch_news_link: %s' % crunch_news_link)
            if (CURRENT_DATE in crunch_news_link):
                news_img = img_tag.img['data-src']
                print('news_img: %s' % news_img)
                # check link is already sent
                ck_st = is_in_newsfile(ck_link=crunch_news_link)
                if not ck_st:
                    write_text_file(
                        _fpath=FILENAME,
                        _write_mode='a',
                        _text=crunch_news_link)
                    tech_news_dict.update({crunch_news_text: [crunch_news_link, news_img]})

    print('[DEBUG] tech_news_dict %s' % tech_news_dict)

    return tech_news_dict, tech_crunch_title


class EmailContents(object):

    def __init__(self, keyPath, sheetName):
        self.techorange_dict, self.techorange_title = get_techorange_news()
        self.ithome_dict, self.ithome_title = get_ithome_news()
        self.bnext_dict, self.bnext_title = get_bnext_news()
        self.inside_dict, self.inside_web_title = get_inside_news()
        self.twtech_news_dict, self.twtech_web_title = get_tw_tech_news()
        self.crunch_news_dict, self.crunch_news_title = get_tech_crunch()

        self.news_contents_dict = {
            'iThome': [self.ithome_title, self.ithome_dict],
            '數位時代': [self.bnext_title, self.bnext_dict],
            'TechCrunch': [self.crunch_news_title, self.crunch_news_dict],
            'Tech News 科技新報': [self.twtech_web_title, self.twtech_news_dict],
            'Tech Orange 科技報橘': [self.techorange_title, self.techorange_dict],
            'INSIDE 硬塞的網路趨勢觀察': [self.inside_web_title, self.inside_dict]
        }

        self.title_style = '<br><b><font style="font-size:150%; ' \
            'color:#FFFF00; background:#000000">' \
            '{title}</font></b><br><br>'
        self.news_style = """
        <a
            href="{link}" style="text-decoration:none; font-size:medium;">
            {news_text}
        </a>
        <br>
        <br>
        """

        self.technews_dict = get_google_sheet_data(keyPath, sheetName)
        self.receiver_mail_list = list(self.technews_dict.keys())

    def get_user_subscribe_news(self, user_mail):
        user_subscribe_news_arr = list()
        if self.technews_dict[user_mail]:
            user_subscribe_news = self.technews_dict[user_mail]
            user_subscribe_news_arr = user_subscribe_news.split(',')
            user_subscribe_news_arr = \
                [content.strip() for content in user_subscribe_news_arr]
        return user_subscribe_news_arr

    def get_mail_contents(self, user_mail):
        _user_email_contents = ""
        mail_contents_overview = list()
        user_news_arr = self.get_user_subscribe_news(user_mail)
        for user_subc_news in user_news_arr:
            news_info = self.news_contents_dict[user_subc_news]
            user_news_title = news_info[0]
            user_news_dict = news_info[1]
            if user_news_dict:
                _user_email_contents += EmailHtmlTemplate.NEWS_TITLE.format(
                    news_title=user_subc_news)
            _user_email_contents += self.check_news_return_value(
                news_title=user_news_title, news_dict=user_news_dict)
            mail_contents_overview.append(user_news_title)

        email_html_contents = EmailHtmlTemplate.NEWS_ROW_TPL.format(
            title="科技新聞 Tech News - " + CURRENT_DATE,
            news_row_data=_user_email_contents,
            tail_sign=EmailHtmlTemplate.TAIL_SIGN)
        # print(email_html_contents)

        return email_html_contents, mail_contents_overview

    def check_news_return_value(self, news_title, news_dict):
        email_contents = ""
        news_dict = news_dict.copy()
        if news_dict:
            while True:
                if len(news_dict) % 2 == 0:
                    _news1 = list(news_dict.popitem())
                    _news2 = list(news_dict.popitem())
                    pair_flag = True
                else:
                    _news1 = list(news_dict.popitem())
                    pair_flag = False

                news_link1 = _news1[1][0]
                news_img1 = _news1[1][1]
                news_tag1 = _news1[0].split('-')[0].replace('[', '').replace(']', '').strip()
                news_title1 = _news1[0].split('-')[1].strip()
                email_img_html1 = EmailHtmlTemplate.IMG_TAG.format(
                    img_link=news_img1, news_link=news_link1)
                news_text_html1 = EmailHtmlTemplate.NEWS_TAG.format(
                    news_title=news_tag1, news_descrip=news_title1, news_link=news_link1)

                if pair_flag:
                    news_link2 = _news2[1][0]
                    news_img2 = _news2[1][1]
                    news_tag2 = _news2[0].split('-')[0].replace('[', '').replace(']', '').strip()
                    news_title2 = _news2[0].split('-')[1].strip()
                    email_img_html2 = EmailHtmlTemplate.IMG_TAG.format(
                        img_link=news_img2, news_link=news_link2)
                    news_text_html2 = EmailHtmlTemplate.NEWS_TAG.format(
                        news_title=news_tag2, news_descrip=news_title2, news_link=news_link2)

                    email_contents += EmailHtmlTemplate.NEWS_ROW_DATA_PAIR.format(
                        left_img_tag=email_img_html1, left_news_data=news_text_html1,
                        right_img_tag=email_img_html2, right_news_data=news_text_html2)
                else:
                    email_contents += EmailHtmlTemplate.NEWS_ROW_DATA_ODD.format(
                        left_img_tag=email_img_html1, left_news_data=news_text_html1)

                # check if news_dict length
                if len(news_dict) == 0:
                    break

        return email_contents

    def get_recipient_list(self):
        return self.receiver_mail_list


def get_google_sheet_data(keyPath, sheetName):
    google_dirve = GoogleDrive(keyPath, sheetName)
    sheet_data = google_dirve.google_sheet_read()
    log.info('Sheet data: %s' % sheet_data)

    subscribe_dict = dict()

    for i, data_i in enumerate(sheet_data):
        if i == 0:
            continue
        subscribe_news = data_i[4]
        subscribe_status = data_i[2]
        subscribe_mail = data_i[1]

        if subscribe_mail not in subscribe_dict and subscribe_status == 'Yes':
            subscribe_dict.update({subscribe_mail: subscribe_news})

    log.info('')
    log.info('subscribe_dict = %s' % subscribe_dict)

    return subscribe_dict


def write_text_file(_fpath, _write_mode, _text):
    with open(_fpath, _write_mode) as _f:
        _f.write('%s\n' % _text)
        _f.close()


def is_in_newsfile(ck_link):
    if os.path.exists(FILENAME):
        f = open(FILENAME)
        flines = f.readlines()
        f.close()
        data_list = [fdata.strip() for fdata in flines]
        check_status = (ck_link in data_list)

    else:
        print('[ DEBUG ] File not exist')
        check_status = False

    print('[ DEBUG ] [ %s ] -> Link=%s' % (check_status, ck_link))

    return check_status


def main(keyPath, sheetName):
    print('[ DEBUG ] >>>>>>>>>> %s <<<<<<<<<<' % CURRENT_DATE)
    subscribe_all_news_list = list()
    subscribe_all_mail_contents = ""
    user_info = EmailContents(keyPath, sheetName)
    news_def_len = len(user_info.news_contents_dict)
    receiver_mail_list = user_info.get_recipient_list()

    for user_mail_in_sheet in receiver_mail_list:
        email_text, email_overview = \
            user_info.get_mail_contents(user_mail=user_mail_in_sheet)
        ov_len = len(email_overview)

        if ov_len == news_def_len:
            subscribe_all_news_list.append(user_mail_in_sheet)
            subscribe_all_mail_contents = email_text
        else:
            # Send mail to subscription personal selected
            print('\n[ DEBUG ] Subscribe <Personal> %s - %s\n' %
                  (user_mail_in_sheet, email_overview))

            if email_text is not "":
                utils.smtp_sender(send_email=s_email,
                                  send_pwd=s_pwd,
                                  recv_email=[user_mail_in_sheet],
                                  mesg_text=email_text,
                                  subject="科技新聞 Tech News - " + CURRENT_DATE,
                                  subtype='html')
            else:
                print("Mail not sent.")

    # Send mail to subscribe all news user
    print('[ DEBUG ] Subscribe <All> user -> %s' % subscribe_all_news_list)
    if subscribe_all_mail_contents is not "":
        utils.smtp_sender(send_email=s_email,
                          send_pwd=s_pwd,
                          recv_email=subscribe_all_news_list,
                          mesg_text=subscribe_all_mail_contents,
                          subject="科技新聞 Tech News - " + CURRENT_DATE,
                          subtype='html')
    else:
        print("Mail not sent.")


if __name__ == '__main__':

    if len(sys.argv) > 4:
        key_path = sys.argv[1]
        sheet_name = sys.argv[2]
        s_email = sys.argv[3]
        s_pwd = sys.argv[4]

        # Remove other days news file
        if not os.path.exists(FILENAME):
            print('[ DEBUG ] Remove file %s' % NEWSFILE_ALL)
            os.popen('rm %s' % NEWSFILE_ALL)

        main(keyPath=key_path, sheetName=sheet_name)

    else:
        print("Usage: %s key_path SheetName SenderEmail SenderPwd" %
              sys.argv[0])
        exit()
