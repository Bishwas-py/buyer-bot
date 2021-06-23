import imaplib
import email
from decouple import config


host = 'imap.gmail.com'
username = config("G_EMAIL")
password = config("G_PASSWORD")

mail = imaplib.IMAP4_SSL(host)
mail.login(username, password)

mail.select("inbox")


class FindWith(object):
    """
    Set of supported search strategies.
    """
    BESTBUY = "Fwd: Your Password Reset verification code"

def get_verification_code(find_with:str):
    _, search_data = mail.search(None, 'SUBJECT', f'"{find_with}"')
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
                    verification_code = msg_body.split("Verification Code:")[-1].split('*')[0].strip('\r\n')
        
    return verification_code

if __name__ == "__main__":
    all_inbox_msg = get_verification_code(FindWith.BESTBUY)
    print(all_inbox_msg)