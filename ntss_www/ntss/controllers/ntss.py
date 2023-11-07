"""
The NTSS package is the main controller that users access when first accessing the site.
"""
from ntss.controllers.controller import BaseController
from ntss.views.ntss import NtssViews
from ntss.controllers.users import UsersController
from ntss.models.session import Session


class NtssController(BaseController):
    """
    The NTSS controller is the default controller that is accessed
    """

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
                print('valid login')
                return self._redirect('/dashboard')
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
        user_ctrl = UsersController(self._request)
        if user_ctrl.validate_user(email, password) and user_ctrl.has_access('dashboard'):
            self._create_session(user_ctrl)
            error_msg = None
        if not email:
            error_msg = 'Email is required'
        elif not password:
            error_msg = 'Password is required'
        return email, password, error_msg

    def logout(self):
        """
        Logout the user and redirect to the login page
        """
        """
        Make sure to destroy the session for the user
        """
        session_id = self._get_session_id()
        Session().delete_session(session_id)
        return self._redirect('/')

    def dashboard(self):
        """
        Load the Dashboard for a User
        """
        return NtssViews().dashboard()

    def _create_session(self, user_controller):
        """
        Creates a session for the current user
        """
        user_controller.create_session()

    def _get_session_id(self):
        cookies = self._load_cookies()
        print(cookies)
        session_id = 'xxxx'
        return session_id

    def _get_session_data(self, session_id):
        return Session().get_session(session_id)
