"""
The base controller that other controllers should inherit from
"""
from http import cookiejar
import json
from webob import exc
from ntss.config.constants import COOKIE_INFO


class BaseController:
    """
    The base controller
    """
    _cookies = {}
    _request = None

    def __init__(self, request, response):
        """
        Checks if the user is logged in and if not redirects them
        Also verifies that the user has access
        """
        self._request = request
        self._response = response
        self._load_cookies()

    def _load_cookies(self):
        """
        Load cookies from the browser
        """
        cookiejar.CookieJar().clear_expired_cookies()
        self._cookies = self._request.cookies

    def _add_cookie(
            self,
            cookie_value: str | dict | list,
            cookie_name: str = None
            ):
        """
        Set a cookie to send to the browser
        """
        cookie_data = cookie_value
        if type(cookie_value) in [dict, list]:
            cookie_data = json.dumps(cookie_value)
        if cookie_name is None:
            cookie_name = COOKIE_INFO['name']
        cookie_settings = {
            'name': cookie_name,
            'value': cookie_data,
            'path': '/',
            'secure': True,
            'httponly': True,
            'max_age': COOKIE_INFO['max_age'],
            'samesite': 'strict'
        }
        self._response.set_cookie(**cookie_settings)
        return self._response

    def _clear_login_cookie(self):
        if self._cookies and COOKIE_INFO['name'] in self._cookies.keys() \
                and self._cookies.get(COOKIE_INFO['name']):
            self._response.delete_cookie(COOKIE_INFO['name'])

    def is_logged_in(self):
        """
        Checks if the user is currently logged in
        """
        if self._cookies and COOKIE_INFO['name'] in self._cookies.keys() and \ 
                self._cookies.get(COOKIE_INFO['name']):
            return True
        return False

    def redirect(self, path):
        if not path.startswith('/'):
            path = '/' + path

        redirect = exc.HTTPSeeOther(
            location=path,
            detail=f'Redirecting To {path}',
            headers=self._response.headers
            )
        return redirect

    def get_permissions(self):
        """
        Retrieves the permissions for the user
        """
        return False

    def has_access(self, path: str) -> bool:
        """
        Checks if the user has access for the page requested
        This should be based on the permissions and route
        """
        role_paths = ['/', '/logout', '/dashbaord']
        if path in role_paths:
            return True
        return False
