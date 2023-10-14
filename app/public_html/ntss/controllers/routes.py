from typing import Any
from parse import parse
from webob import Request, Response
from ntss.config.constants import ALL_HTTP_METHODS
from ntss.views.routes import RouteViews

class Routes():

    def __init__(self):
        """
        Instanciate routes and methods
        """
        self._routes = {}
        self._http_methods = []

    def route(self, path, methods=None):
        """
        Handles adding paths and handlers to a route
        """
        self._http_methods = self._set_http_methods(methods)
        
        if path in self._routes:
            raise AssertionError(f'Route {path} already exists.')
        
        def wrapper(handler):
            self._routes[path] = {'http_methods': self._http_methods, 'handler': handler}
            return handler

        return wrapper
    
    def _set_http_methods(self, methods):
        """
        Sets the routes accepted for the path
        """
        if methods is None:
            methods = ALL_HTTP_METHODS
        
        accepted_methods = [method.upper() for method in methods if method.upper() in ALL_HTTP_METHODS]
        return accepted_methods

    def __call__(self, environ, start_response) -> Any:
        """
        This handles the incoming request from wsgi.
        """
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request) -> Response:
        """
        Takes the incoming request searches for the handler
        If the handler if found it's returned, otherwise the default response is returned
        """
        response = Response()
        
        handler = None

        if request.method not in self._http_methods:
            self.default_response(response)
        else:
            handler, kwargs = self._get_handler(request.path, request.method)

        if handler:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response
    
    def _get_handler(self, request_path, request_method):
        """
        This loads the function from the main.py file that maps to the requested path
        """
        for path, path_dict in self._routes.items():
            accepted_methods, handler = path_dict.values()
            print(accepted_methods)
            print(request_method)
            print(request_method in accepted_methods)
            parse_result = parse(path, request_path)
            if parse_result and request_method in accepted_methods:
                return handler, parse_result.named
        return None, None

    def default_response(self, response):
        """
        The default reponse is to load a 404 page
        """
        response.status_code = 404
        response.text = RouteViews().error_page()
        