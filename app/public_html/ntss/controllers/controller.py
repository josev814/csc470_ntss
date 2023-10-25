"""
The base controller that other controllers should inherit from
"""
from http import cookiejar
import os

class BaseController:
    """
    The base controller
    """
    _cookies = {}
    def __init__(self):
        """
        Checks if the user is logged in and if not redirects them
        Also verifies that the user has access
        """
        self._load_cookies()
        if not self.is_logged_in() and not self.get_permissions():
            # redirect to home to login
            pass
        if not self.has_access():
            # load a view for access denied
            pass

    def _load_cookies(self):
        """
        Load cookies from the browser
        """
        cookiejar.CookieJar().clear_expired_cookies()
        if 'HTTP_COOKIE' in os.environ:
            cookies = os.environ['HTTP_COOKIE'].split('; ')
            for cookie in cookies:
                cookie = cookie.split('=')
                self._cookies[cookie[0]] = cookie[1]

    def is_logged_in(self):
        """
        Checks if the user is currently logged in
        """
        if 'logged_in' in self._cookies and self._cookies['logged_in'] == 'True':
            return True
        return False

    def get_permissions(self):
        """
        Retrieves the permissions for the user
        """
        return False

    def has_access(self):
        """
        Checks if the user has access for the page requested
        This should be based on the permissions and route
        """
        return False
