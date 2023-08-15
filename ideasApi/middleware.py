import logging

logger = logging.getLogger(__name__)

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("API request: %s %s", request.method, request.path)
        response = self.get_response(request)
        return response
