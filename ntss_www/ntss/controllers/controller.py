"""
The base controller that other controllers should inherit from
"""
from webob import Response, exc
from http import cookiejar
import json
from ntss.config.constants import COOKIE_INFO


class BaseController:
    """
    The base controller
    """
    _cookies = {}
    _request = None

    def __init__(self, request):
        """
        Checks if the user is logged in and if not redirects them
        Also verifies that the user has access
        """
        self._request = request
        self._load_cookies()
        if request.path == '/':
            if not self.is_logged_in() and not self.get_permissions():
                Response.location = '/'
                # redirect to home to login
        elif not self.has_access(request.path):
            # load a view for access denied
            pass

    def _load_cookies(self):
        """
        Load cookies from the browser
        """
        cookiejar.CookieJar().clear_expired_cookies()
        self._cookies = self._request.cookies

    def _add_cookie(
            self, response: Response,
            cookie_value: str | dict | list,
            cookie_name: str | None = None
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
        response.set_cookie(**cookie_settings)
        return response

    def is_logged_in(self):
        """
        Checks if the user is currently logged in
        """
        print(self._cookies.keys())
        if self._cookies and 'logged_in' in self._cookies.keys() and self._cookies.get('logged_in'):
            return True
        return False

    def _redirect(self, path):
        if not path.startswith('/'):
            path = '/' + path

        redirect = exc.HTTPSeeOther(location=path)
        return redirect

    def get_permissions(self):
        """
        Retrieves the permissions for the user
        """
        return False

    def has_access(self, path):
        """
        Checks if the user has access for the page requested
        This should be based on the permissions and route
        """
        return True
