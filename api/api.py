import inspect
from typing import Any, Tuple

from requests import Session as RequestsSession
from parse import parse
from webob import Request, Response
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from app.urls import URLS
from api.views import View
from api.router.api_route import APIRoute


class MoviesAPI:
    def __init__(self):
        self._routes: list[APIRoute] = URLS
        self._session = None

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def get_handler(self, request) -> Tuple[View, dict | Any]:
        request_path = request.path
        for route in self._routes:
            parse_result = parse(route.path, request_path)
            if parse_result:
                return route.view, parse_result.named

        return None, None

    def handle_request(self, request) -> Response:
        response = Response()

        handler, kwargs = self.get_handler(request)

        if handler is not None:
            if inspect.isclass(handler):
                # Allow to manage basic permission for authenticated or not users
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method Not Allowed", request.method)

                response = handler(request, response, **kwargs)

        else:
            response.status_code = 404
            response.text = "404 Not Found"

        return response

    def session(self, base_url="http://testserver"):
        """
        Cached Testing HTTP client based on Requests by Kenneth Reitz.
        """

        if self._session is None:
            session = RequestsSession()
            session.mount(base_url, RequestsWSGIAdapter(self))
            self._session = session

        return self._session
