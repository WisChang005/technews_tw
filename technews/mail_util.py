import smtplib
import logging
from functools import wraps
from email.header import Header
from email.mime.text import MIMEText


class SendEmailRetryTimeout(Exception):
    pass


def error_retry(func):
    @wraps(func)
    def warps_func(*args, **kwargs):
        for i in range(3):
            try:
                rlt = func(*args, **kwargs)
            except Exception as e:
                logging.exception(e)
                logging.warning("Retry Func.%s, [%s]", func.__name__, i)
            else:
                break
        else:
            raise SendEmailRetryTimeout("Function retry failed.")
        return rlt
    return warps_func


def get_smtp_server(sender):
    smtp_server = {
        "hotmail": "smtp-mail.outlook.com",
        "gmail": "smtp.gmail.com"
    }
    smtp_srv = None
    for k, v in smtp_server.items():
        if k in sender:
            smtp_srv = v
            break
    else:
        raise ValueError(f"Invalid Email Address [{sender}]")

    logging.debug("Used SMTP server -> %s", smtp_srv)
    return smtp_srv


@error_retry
def mail_sender(sender, sender_pwd, recv_email, mesg_contents, subject, msg_type):
    """ SMTP send e-mail with smtp server "smtp.live.com"
    Args:
        send_email: sender email username.
        send_pwd: sender email password.
        recv_email: receiver email address.
        mesg_text: email message contents.
        subject: subject title.
        subtype: subtype can be plain, html...etc.
    """
    logging.debug("Send Mail by -> %s", sender)
    logging.debug("Send Email to -> %s", recv_email)

    smtp_srv = get_smtp_server(sender)
    message = MIMEText(mesg_contents, msg_type, "utf-8")
    message["From"] = Header(sender)
    message["Subject"] = Header(subject)

    server = smtplib.SMTP(smtp_srv, 587, timeout=30)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, sender_pwd)

    server.sendmail(sender, recv_email, message.as_string())
    server.quit()
    logging.info("Send mail successful!")
