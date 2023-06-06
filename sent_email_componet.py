import os
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.base import MIMEBase
from email import encoders


def email_attachment(content):
    email_sender = 'kuva5008@gmail.com'
    email_pw = os.environ.get("Email_password")
    email_receiver = 'area51.cu@gmail.com'
    subject = 'Congrats, you got a new customer. Check attachment for details'
    body = f'{content}'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Define the file to attach
    filename = 'Amet_data.xlsx'

    # coding to send attachment
    with open('Amet_data.xlsx', 'rb') as fp:  # r is for read and b for binary
        pdf_data = fp.read()
        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        em.add_attachment(pdf_data,
                          maintype=maintype,
                          subtype=subtype,
                          filename=filename)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pw)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    print('email with attachment sent')
    return True


def email_simple(content):
    email_sender = 'kuva5008@gmail.com'
    email_pw = os.environ.get("Email_password")
    email_receiver = 'area51.cu@gmail.com'
    subject = 'Congrats. You got a new admirer'
    body = f'{content}'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pw)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    print('email about the fan sent')
    return True
