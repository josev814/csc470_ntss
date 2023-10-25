"""
This package handles the route requests
"""
from typing import Any
import os
from parse import parse
from webob import Request, Response
from ntss.config.constants import ALL_HTTP_METHODS
from ntss.views.routes import RouteViews

class Routes():
    """
    This class handles the route requests and response to the server
    """
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
        
        accepted_methods = [
            method.upper() for method in methods if method.upper() in ALL_HTTP_METHODS
        ]
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
        if request.path.startswith('/static'):
            self._load_file(request, response)
            return response
        
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
    
    def _load_file(self, request, response):
        """
        Loads a static file
        """
        www_path='/var/www/html/public_html'
        if not os.path.isfile(f'{www_path}{request.path}'):
            self.default_response(response)
        else:
            response.status_code = 200
            if request.path.endswith('css'):
                response.content_type = 'text/css'
            elif request.path.endswith('js'):
                response.content_type = 'text/js'
            
            response.text = ''
            with open(f'{www_path}{request.path}', 'r', encoding='utf-8') as file_handler:
                response.text = file_handler.read()
