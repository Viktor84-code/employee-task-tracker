from celery import shared_task
from django.core.mail import send_mail


@shared_task
def notify_task_created(task_id, assignee_email, message):
    """
    Отправляет email уведомление о создании задачи.
    """
    if not assignee_email:
        raise ValueError("Email получателя не может быть пустым.")

    send_mail(
        subject='Новая задача',
        message=message,
        from_email='noreply@taskflow.com',
        recipient_list=[assignee_email],
        fail_silently=False,
    )


@shared_task
def notify_task_status_changed(task_id, creator_email, message):
    """
    Отправляет email уведомление о смене статуса задачи.
    """
    if not creator_email:
        raise ValueError("Email получателя не может быть пустым.")

    send_mail(
        subject='Статус задачи изменён',
        message=message,
        from_email='noreply@taskflow.com',
        recipient_list=[creator_email],
        fail_silently=False,
    )
