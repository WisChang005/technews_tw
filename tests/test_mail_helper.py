import json

from technews.mail_helper import EmailContentHelper


def _load_samples(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def test_orange_email_helper():
    mh = EmailContentHelper()

    samples_list = [
        "ithome_samples.json",
        "business_samples.json",
        "inside_samples.json"
    ]

    news_rows = ""
    for sp_name in samples_list:
        samples = _load_samples(f"tests/samples/{sp_name}")
        news_rows += mh.get_news_html_contents(samples, samples["news_page_title"])

    email_html = mh.get_email_html("2024-科技新聞", news_rows)
    with open("news_email.html", "w", encoding="utf-8") as f:
        f.write(email_html)
