from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_notification(recipient_email, subject, message):
    """
    Отправляет email уведомление.
    """
    if not recipient_email:
        raise ValueError("Email получателя не может быть пустым.")

    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@taskflow.com',
        recipient_list=[recipient_email],
        fail_silently=False,
    )
