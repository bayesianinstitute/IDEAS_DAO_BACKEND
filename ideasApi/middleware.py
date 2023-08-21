import logging
import ipaddress
from django.utils.deprecation import MiddlewareMixin
import re
from rest_framework.response import Response
from ipware import get_client_ip
from django.urls import resolve

logger = logging.getLogger(__name__)

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("API request: %s %s", request.method, request.path)
        response = self.get_response(request)
        return response
    
class ProxyDetectionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.proxy_logger = logging.getLogger('proxy_logger')

    def __call__(self, request):
        client_ip, is_routable = get_client_ip(request)
        request.is_request_from_proxy = False
        request.client_ip = client_ip
        request.is_routable = is_routable

        if is_routable is False and client_ip:
            endpoint_url = request.path_info  # Get the URL path
            request.is_request_from_proxy = True
            self.proxy_logger.error("Request from proxy: Client IP %s for URL %s", client_ip, endpoint_url)

        response = self.get_response(request)
        return response

    
    
# class ProxyDetectionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.proxy_logger = logging.getLogger('proxy_logger')  # Get the proxy_logger logger

#     def __call__(self, request):
#         client_ip, is_routable = get_client_ip(request)
#         request.is_request_from_proxy = False

#         if is_routable is False and client_ip:
#             request.is_request_from_proxy = True
#             self.proxy_logger.error("Request from proxy: Client IP %s", client_ip)

#         response = self.get_response(request)
#         return response









# class ProxyDetectionMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         is_proxy_request = False

#         if 'HTTP_X_FORWARDED_FOR' in request.META:
#             ip_address = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
#             if ipaddress.ip_address(ip_address):
#                 if self.is_private_ip(ip_address):
#                     is_proxy_request = True
#         elif 'REMOTE_ADDR' in request.META:
#             ip_address = request.META['REMOTE_ADDR']
#             if ipaddress.ip_address(ip_address) and self.is_private_ip(ip_address):
#                 is_proxy_request = True

#         if is_proxy_request:
#             logger = logging.getLogger('proxy_logger')
#             log_message = f"API request made from a proxy. IP Address: {ip_address}"
#             logger.error(log_message)
#             return Response({"message": "API request made from a proxy."})

#         # Continue with the request processing
#         return None

#     def is_private_ip(self, ip):
#         private_ranges = [
#             ipaddress.ip_network('10.0.0.0/8'),
#             ipaddress.ip_network('172.16.0.0/12'),
#             ipaddress.ip_network('192.168.0.0/16'),
#         ]
#         for private_range in private_ranges:
#             if ipaddress.ip_address(ip) in private_range:
#                 return True
#         return False

# class ProxyDetectionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if the X-Forwarded-For header exists
#         if 'HTTP_X_FORWARDED_FOR' in request.META:
#             request.is_proxy_request = True
#         else:
#             request.is_proxy_request = False

#         response = self.get_response(request)
#         return response

