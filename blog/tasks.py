from celery import shared_task
from django.core.mail import send_mail
import time


@shared_task
def comment_send_mail_reader(username, email):
    subject = 'Save your comment'
    message = f'Hi {username}, your comment successfully save in my site'
    from_email = 'localhost:8000'
    recipient_list = [email]
    time.sleep(5)
    mail_sent = send_mail(subject, message, from_email, recipient_list)
    return mail_sent


@shared_task
def comment_send_mail_author(title, email, username):
    subject = f'comment for {title}'
    message = f'a comment by {username} for {title} saved'
    from_email = 'localhost:8000'
    recipient_list = [email]
    time.sleep(5)
    mail_sent = send_mail(subject, message, from_email, recipient_list)
    return mail_sent
