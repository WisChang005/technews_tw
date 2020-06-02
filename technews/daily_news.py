import os
import datetime

from technews import mail_util
from technews import TechNews
from technews import EmailContentHelper


def main():
    mh = EmailContentHelper()

    news_list = [
        TechNews("orange").get_today_news,
        TechNews("ithome").get_today_news,
        TechNews("business").get_today_news
    ]

    news_rows = ""
    skip_counts = 0
    for news_getter in news_list:
        news_data = news_getter()
        news_contents = news_data["news_page_title"]
        print(news_data)
        if news_data["news_counts"] == 0:
            skip_counts += 1
            continue
        news_rows += mh.get_news_html_contents(news_data, news_contents)

    if skip_counts == len(news_list):
        print("No any tech news today.")
        return

    date = datetime.date.today().strftime("%Y/%m/%d")
    mail_subject = f"科技新聞 Tech News - {date}"
    email_html = mh.get_email_html(mail_subject, news_rows)

    mail_util.mail_sender(
        os.environ["MAIL_SENDER"],
        os.environ["MAIL_SENDER_PWD"],
        os.environ["MAIL_RECV"].split(","),
        email_html,
        mail_subject,
        "html")
    print("Send Today's Tech News Completed!")


if __name__ == "__main__":
    main()
