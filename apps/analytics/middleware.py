import time
from .models import VisitLog

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = int(time.time() - start_time)

        if request.user.is_authenticated:
            VisitLog.objects.create(
                user=request.user,
                page=request.path,
                path=request.path,
                duration=duration
            )
        return response
