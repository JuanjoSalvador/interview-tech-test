from webob import Request, Response
from http_status import HTTPStatus

class API:
    def __init__(self):
        self._routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        
        return response(environ, start_response)
    
    def route(self, path):
        def wrapper(handler):
            self._routes[path] = handler
            return handler
        return wrapper
    
    def handle_request(self, request):
        response = Response()
        
        handler = self._routes.get(request.path)
        try:
            handler(request, response)
        except KeyError:
            response.status_code = HTTPStatus.HTTP_NOT_FOUND
        except Exception:
            response.status_code = HTTPStatus.HTTP_INTERNAL_SERVER_ERROR

        return response