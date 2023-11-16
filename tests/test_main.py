"""
Testing the Base Controller functionality
"""
import unittest
from os import environ
from webob import Request, Response

from ntss.controllers.controller import BaseController


class NTSSBase(unittest.TestCase):
    """
    The class used for running tests against the controller
    """
    def setUp(self):
        """
        Instead of calling __init__ we call setup
        Anything we define in here is what all the tests need to run
        """
        fake_environ = {}
        for key, val in environ.items():
            fake_environ[key] = val
        self._bc = BaseController(Request(fake_environ), Response())

    def test_not_logged_in(self):
        """
        Testing to ensure that we are not logged in
        """
        self.assertFalse(self._bc.is_logged_in())

    def test_cookies_empty(self):
        """
        The cookies should be empty at this point
        """
        self.assertFalse(self._bc._cookies)

    def test_has_access(self):
        """
        Since the cookies are empty, the user should not have access
        """
        self.assertFalse(self._bc.has_access('/dashboard'))
