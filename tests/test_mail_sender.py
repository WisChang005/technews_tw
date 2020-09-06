import os

import pytest

from technews import mail_util
from technews import TechNews
from technews import EmailContentHelper


@pytest.mark.skip("skip test email")
def test_send_email_function():
    mh = EmailContentHelper()

    samples_list = [
        TechNews("orange").get_news_by_page,
        TechNews("ithome").get_news_by_page,
        TechNews("business").get_news_by_page,
        TechNews("inside").get_news_by_page
    ]

    news_rows = ""
    for sp_name in samples_list:
        samples = sp_name(2)
        news_rows += mh.get_news_html_contents(samples, samples["news_page_title"])

    email_html = mh.get_email_html("Test-科技新聞", news_rows)

    mail_util.mail_sender(
        os.environ["MAIL_SENDER"], os.environ["MAIL_SENDER_PWD"],
        os.environ["MAIL_RECV"].split(","), email_html, "Test-科技新聞", "html")


@pytest.mark.skip("skip test email force error")
def test_send_email_force_error():
    with pytest.raises(mail_util.SendEmailRetryTimeout):
        mail_util.mail_sender("", "", "", "", "Test-科技新聞", "plain")
