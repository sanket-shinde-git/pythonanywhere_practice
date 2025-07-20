 # middleware/request_timer.py

import time
from django.utils.deprecation import MiddlewareMixin

class RequestTimerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("in process_request")
        request.start_time = time.time()  # 145

    def process_response(self, request, response):
        print("in process_response")
        duration = time.time() - getattr(request, 'start_time', time.time())# 145
        print(f"Request took {duration:.2f} seconds")
        return response