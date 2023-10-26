"""
This handles session management
"""
import json
from webob import cookies


class session:
    """
    This class will do session management for users
    """
    def add_session(self):
        """
        Method to add session information
        """
        cookie_name = 'randomizedguid'
        cookie_value = json.dumps({'logged_in': 'true'})
        cookies.make_cookie(cookie_name, cookie_value)

    def update_session(self):
        """
        Makes updates to the session
        """

    def delete_session(self, cookie_name):
        """
        Remove the session if it's expired
        """
        cookies.Cookie(cookie_name).clear()
