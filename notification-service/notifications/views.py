from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_email_notification


class SendNotificationView(APIView):
    """
    Внутренний API для отправки уведомлений.
    """

    def post(self, request):
        """
        Отправляет email уведомление.
        """
        recipient_email = request.data.get('recipient_email')
        subject = request.data.get('subject')
        message = request.data.get('message')

        if not recipient_email or not subject or not message:
            return Response(
                {'error': 'Все поля обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        send_email_notification.delay(recipient_email, subject, message)

        return Response(
            {'message': 'Уведомление отправлено'},
            status=status.HTTP_200_OK
        )
