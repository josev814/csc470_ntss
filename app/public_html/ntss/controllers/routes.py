from typing import Any
from parse import parse
from webob import Request, Response
from ntss.views.routes import RouteViews

class Routes():

    def __init__(self):
        self.routes = {}

    def route(self, path, methods):
        if path in self.routes:
            raise AssertionError(f'Route {path} already exists.')
        
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def __call__(self, environ, start_response) -> Any:
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        
        handler, kwargs = self.get_handler(request.path)

        if handler:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response
    
    def get_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result:
                return handler, parse_result.named
        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = RouteViews().error_page()
        