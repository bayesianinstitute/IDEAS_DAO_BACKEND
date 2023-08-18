import logging
import ipaddress
from django.utils.deprecation import MiddlewareMixin
import re
from rest_framework.response import Response
from ipware import get_client_ip

logger = logging.getLogger(__name__)

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("API request: %s %s", request.method, request.path)
        response = self.get_response(request)
        return response

class ProxyDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip, is_routable = get_client_ip(request)
        request.is_request_from_proxy = False

        if is_routable is False and client_ip:
            request.is_request_from_proxy = True

        print("Request from proxy:", request.is_request_from_proxy)  # Add this line

        response = self.get_response(request)
        return response
