from django.utils.deprecation import MiddlewareMixin

class PublicAccessControlMiddleware(MiddlewareMixin):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Allow-Methods'] = '*'
        response['Access-Control-Max-Age'] = 86400 
        return response