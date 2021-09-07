import imaplib
import email
from bs4 import BeautifulSoup
from time import sleep as wait


class FindWith(object):
    """
    Set of supported search strategies.
    """
    BESTBUY = ('SUBJECT', '"Your Password Reset verification code"', 'FROM', '"emailinfo.bestbuy.com"')


def get_verification_code(item, find_with:str):
    host = 'imap.gmail.com'
    username = item.account.email
    password = item.account.g_password
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, *find_with)
    verification_code = 0

    for num in search_data[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        email_msg = email.message_from_bytes(b)

        for part in email_msg.walk():
            if part.get_content_type()=="text/plain":
                body = part.get_payload(decode=True)
                msg_body = body.decode()
                if FindWith.BESTBUY == find_with and "Verification Code:" in msg_body:
                    print("Waiting for 5 secs... ")
                    wait(5)
                    verification_code = msg_body.split("Verification Code:")[-1].split('*')[0].strip('\r\n')
            elif part.get_content_type()=="text/html":
                body = part.get_payload(decode=True)
                msg_body = BeautifulSoup(body.decode(), 'html5lib').findAll(text=True)
                verification_code = list(set([word for word in msg_body if word.isdigit()]))[0]
                if FindWith.BESTBUY == find_with and "Verification Code:" in msg_body:
                    print("Waiting for 5 secs... ")
                    wait(5)
                    verification_code = msg_body.split("Verification Code:")[-1].split('*')[0].strip('\r\n')
    # mail.store(num, '+FLAGS', '\\Deleted')
    # mail.expunge()
    # mail.close()
    # mail.logout()
    print(verification_code)
    return verification_code