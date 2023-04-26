import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class Emailer:
    def __init__(self, username, password, smtp_server='smtp.gmail.com', smtp_port=465 ):
        self.username = username
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, to, subject, message, files=[]):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(f.split("/")[-1]))
            msg.attach(part)
        smtp_obj = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        smtp_obj.login(self.username, self.password)
        smtp_obj.sendmail(self.username, to, msg.as_string())
        smtp_obj.quit()