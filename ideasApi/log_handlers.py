import logging
from django.core.mail import send_mail
from django.conf import settings

class MinimalEmailHandler(logging.Handler):
    def emit(self, record):
        error_message = self.format(record)
        subject = 'Error Notification'
        message = f'An error occurred:\n\n{error_message}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [admin[1] for admin in settings.ADMINS], fail_silently=True)
