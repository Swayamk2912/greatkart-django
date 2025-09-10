from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email):
    subject = "Welcome to GreatKart 🎉"
    message = "Thanks for registering with us. Enjoy shopping!"
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)
    return f"Sent to {user_email}"
