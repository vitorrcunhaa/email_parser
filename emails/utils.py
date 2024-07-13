import imaplib
import email
import re
from .models import EmailData
import logging


logger = logging.getLogger('emails')


# It's ok to leave this info here, it is a test account
EMAIL_USER = 'usetwelvetest@gmx.com'
EMAIL_PASS = 'usetwelvetest'
EMAIL_SERVER = 'imap.gmx.com'


def fetch_emails():
    logger.info('Starting to fetch emails')
    try:
        mail = imaplib.IMAP4_SSL(EMAIL_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        logger.info('Logged into email server and selected inbox')

        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        logger.info(f'Found {len(email_ids)} emails to process')

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/html":
                                body = part.get_payload(decode=True).decode()
                                parse_email(body)
                    else:
                        body = msg.get_payload(decode=True).decode()
                        parse_email(body)
            mail.store(email_id, '+FLAGS', '\\Deleted')
            logger.info(f'Processed and marked email {email_id} as deleted')

        mail.expunge()
        mail.close()
        mail.logout()
        logger.info('Finished fetching and processing emails')
    except Exception as e:
        logger.error(f'An error occurred while fetching emails: {e}', exc_info=True)


def parse_email(body):
    try:
        name_match = re.search(r'([A-Za-z ]+) sent you', body)
        amount_match = re.search(r'\$([0-9]+\.[0-9]+)', body)
        comments_match = re.search(r'comments: (.*?)<', body)

        name = name_match.group(1) if name_match else "Unknown"
        amount = float(amount_match.group(1)) if amount_match else 0
        comments = comments_match.group(1) if comments_match else ""
        if name and name != "Unknown" and amount and amount > 0:
            EmailData.objects.create(name=name, amount=amount, comments=comments)
        else:
            logger.info(f'Email not created due to invalid data: name={name}, amount={amount}, comments={comments}')
        logger.info(f'Parsed and saved email: name={name}, amount={amount}, comments={comments}')
    except Exception as e:
        logger.error(f'An error occurred while parsing email: {e}', exc_info=True)
