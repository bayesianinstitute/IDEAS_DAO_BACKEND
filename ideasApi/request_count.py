import time
from django.conf import settings
from django.core.mail import send_mail

class RequestCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = []
    
    def __call__(self, request):
        current_time = time.time()
        self.requests = [timestamp for timestamp in self.requests if current_time - timestamp <= 60]
        
        if len(self.requests) >= settings.REQUEST_THRESHOLD:
            # Send an email to notify about high request volume
            subject = 'High Request Volume Alert'
            message = 'The server is experiencing a high volume of requests.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [admin[1] for admin in settings.ADMINS]  # Extract admin email addresses
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        else:
            self.requests.append(current_time)
            response = self.get_response(request)
            return response
