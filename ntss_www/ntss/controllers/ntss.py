"""
The NTSS package is the main controller that users access when first accessing the site.
"""
from ntss.controllers.controller import BaseController
from ntss.views.ntss import NtssViews
from ntss.controllers.users import UsersController
from ntss.models.session import Session
from ntss.config.constants import COOKIE_INFO


class NtssController(BaseController):
    """
    The NTSS controller is the default controller that is accessed
    """

    _session_id = None

    def login(self):
        """
        Display the login page
        """
        email = None
        password = None
        errors = None
        if self._request.method == 'POST':
            email, password, errors = self._validate_login()
            if not errors:
                return self.redirect('/dashboard')
        return NtssViews().login_view(email, password, errors)

    def _validate_login(self):
        email = None
        password = None
        error_msg = 'Invalid Credentials Provided'
        for request_name, request_value in self._request.params.items():
            match request_name:
                case 'email':
                    email = request_value
                case 'password':
                    password = request_value
        user_ctrl = UsersController(self._request, self._response)
        if user_ctrl.validate_user(email, password) and user_ctrl.has_access('/dashboard'):
            self._create_session(user_ctrl)
            self._add_cookie(self._session_id)
            error_msg = None
        if not email:
            error_msg = 'Email is required'
        elif not password:
            error_msg = 'Password is required'
        return email, password, error_msg

    def logout(self):
        """
        Logout the user and redirect to the login page

        Make sure to destroy the session for the user
        """
        session_id = self._get_session_id()
        Session().delete_session(session_id)
        self._clear_login_cookie()
        return self.redirect('/')

    def dashboard(self):
        """
        Load the Dashboard for a User
        """
        return NtssViews().dashboard()

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
