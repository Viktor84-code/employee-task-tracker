from django.core import mail
from django.test import TestCase
from unittest.mock import patch

from .tasks import send_email_notification


class SendEmailNotificationTest(TestCase):

    def test_send_email_success(self):
        send_email_notification(
            recipient_email='user@example.com',
            subject='Тест',
            message='Привет!',
        )
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.subject, 'Тест')
        self.assertEqual(sent.body, 'Привет!')
        self.assertEqual(sent.to, ['user@example.com'])
        self.assertEqual(sent.from_email, 'noreply@taskflow.com')

    def test_send_email_raises_when_email_none(self):
        with self.assertRaises(ValueError):
            send_email_notification(
                recipient_email=None,
                subject='Тест',
                message='Привет!',
            )

    def test_send_email_raises_when_email_empty(self):
        with self.assertRaises(ValueError):
            send_email_notification(
                recipient_email='',
                subject='Тест',
                message='Привет!',
            )

    def test_send_email_empty_subject(self):
        send_email_notification(
            recipient_email='user@example.com',
            subject='',
            message='Сообщение',
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '')

    def test_send_email_calls_send_mail_once(self):
        with patch('notifications.tasks.send_mail') as mock_send_mail:
            send_email_notification(
                recipient_email='user@example.com',
                subject='Тест',
                message='Сообщение',
            )
            mock_send_mail.assert_called_once_with(
                subject='Тест',
                message='Сообщение',
                from_email='noreply@taskflow.com',
                recipient_list=['user@example.com'],
                fail_silently=False,
            )

    def test_send_email_does_not_call_send_mail_on_missing_email(self):
        with patch('notifications.tasks.send_mail') as mock_send_mail:
            with self.assertRaises(ValueError):
                send_email_notification(
                    recipient_email=None,
                    subject='Тест',
                    message='Сообщение',
                )
            mock_send_mail.assert_not_called()

    def test_send_email_multiple_sends(self):
        send_email_notification(
            recipient_email='one@example.com',
            subject='Первое',
            message='1',
        )
        send_email_notification(
            recipient_email='two@example.com',
            subject='Второе',
            message='2',
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, ['one@example.com'])
        self.assertEqual(mail.outbox[1].to, ['two@example.com'])

    def test_send_email_unicode_content(self):
        send_email_notification(
            recipient_email='user@example.com',
            subject='Уведомление о задаче',
            message='Задача «Важная» завершена.',
        )
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.subject, 'Уведомление о задаче')
        self.assertEqual(sent.body, 'Задача «Важная» завершена.')

    def test_send_email_whitespace_email_not_raised(self):
        send_email_notification(
            recipient_email='   ',
            subject='Тест',
            message='Привет!',
        )
        self.assertEqual(len(mail.outbox), 1)