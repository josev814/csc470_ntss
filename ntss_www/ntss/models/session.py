"""
This handles session management
"""
import json
from webob import cookies


class session:

    def add_session(self):
        cookie_name = 'randomizedguid'
        cookie_value = json.dumps({'logged_in': 'true'})
        cookies.make_cookie(cookie_name, cookie_value)
