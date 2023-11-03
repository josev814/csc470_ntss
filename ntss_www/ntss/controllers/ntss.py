"""
The NTSS package is the main controller that users access when first accessing the site.
"""
from ntss.controllers.controller import BaseController
from ntss.views.ntss import NtssViews
from ntss.controllers.users import UsersController


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
        return NtssViews().login_view(email, password)

    def _validate_login(self):
        email = None
        password = None
        error_msg = 'Invalid Credentials'
        for request_name, request_value in self._request.params.items():
            match request_name:
                case 'email':
                    email = request_value
                case 'password':
                    password = request_value
        if UsersController(self._request).validate_user(email, password) and \
                UsersController(self._request).has_access('dashboard'):
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
        return self._redirect('/')

    def dashboard(self):
        """
        Load the Dashboard for a User
        """
        return NtssViews().dashboard()
