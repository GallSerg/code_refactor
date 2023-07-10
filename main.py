import email
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailActivity:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.smtp = "smtp.gmail.com"
        self.imap = "imap.gmail.com"
        self.smtp_port = 587

    def send_message(self, subject, from_msg, recipients, message):
        msg = MIMEMultipart()
        msg['From'] = from_msg
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        ms = smtplib.SMTP(self.smtp, self.smtp_port)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login, msg['To'], msg.as_string())
        ms.quit()

    def receive_message(self, header=None):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.login, self.password)
        mail.list()
        mail.select()
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.search(None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(str(raw_email))
        mail.logout()
        return email_message


if __name__ == '__main__':
    login = input("Input your login ")
    password = input("Input your password ")
    emails = EmailActivity(login, password)
    emails_theme = input("Input email subject ")
    emails_msg = input("Input email message ")
    emails.send_message(emails_theme, login, ['i@sgalchin.ru', 'warlik.galchin@yandex.ru'], emails_msg)
    print(emails.receive_message('otrs'))
