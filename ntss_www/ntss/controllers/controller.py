"""
The base controller that other controllers should inherit from
"""
from http import cookiejar
import json
from webob import exc
from ntss.models.session import Session
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
        self._session_id = None
        self._session_data = None
        sid = self._get_session_id()

        if not sid:
            if not hasattr(self._request, 'path') or \
                    self._request not in ['/', '/forgot_password', '/register']:
                self.redirect('/')
        elif sid:
            self._session_data = self._get_session_data(sid)
            if not self._session_data and \
                    self._request.path not in ['/', '/forgot_password', '/register']:
                self._delete_session(sid)
                self._clear_login_cookie()
                self.redirect('/')
            elif self._session_data:
                self._add_cookie(sid)
                self._extend_session(sid)

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

    def _get_cookie(self, cookie_name: str):
        """
        Gets a loaded cookie's value
        """
        cookiejar.CookieJar().clear_expired_cookies()
        cookie_value = ''
        if self._cookies and cookie_name in self._cookies.keys() \
                and self._cookies.get(cookie_name):
            cookie_value = self._cookies.get(cookie_name)
        return cookie_value

    def _clear_login_cookie(self):
        if self._cookies and COOKIE_INFO['name'] in self._cookies.keys():
            self._response.delete_cookie(COOKIE_INFO['name'])

    def is_logged_in(self):
        """
        Checks if the user is currently logged in
        """
        if self._cookies and COOKIE_INFO['name'] in self._cookies.keys():
            return True
        return False

    def redirect(self, path):
        """
        Method to redirect to another path
        """
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

    def _create_session(self, user_ctrl):
        """
        Creates a session for the current user
        """
        self._session_id = user_ctrl.create_session()

    def _get_session_id(self):
        """
        Gets the session id for the current session
        """
        self._load_cookies()
        session_id = self._get_cookie(COOKIE_INFO['name'])
        return session_id

    def _get_session_data(self, session_id):
        """
        Returns the session data
        """
        return Session().get_session(session_id)

    def _delete_session(self, session_id):
        """
        Delete the session data
        """
        Session().delete_session(session_id)

    def _extend_session(self, session_id):
        """
        Extend the expiration of the session data
        """
        Session().set_key_expiration(session_id)
