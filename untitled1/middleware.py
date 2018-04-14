class MyMiddleware:
    def process_response(self, request, response):
        response['Service-Worker-Allowed'] = '/'
        return response