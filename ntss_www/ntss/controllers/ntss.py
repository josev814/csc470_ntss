"""
The NTSS package is the main controller that users access when first accessing the site.
"""
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage
# Our own controllers
from ntss.controllers.controller import BaseController
from ntss.views.ntss import NtssViews
from ntss.controllers.users import UsersController
from ntss.config.constants import SITE_INFO


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
        self._delete_session(session_id)
        self._clear_login_cookie()
        return self.redirect('/')
    
    def forgot_password(self):
        """
        Display the forgot password page
        """
        user_email = None
        message = None
        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                match request_name:
                    case 'email':
                        user_email = request_value
            user_ctrl = UsersController(self._request, self._response)
            if user_email and user_ctrl.valid_user(email=user_email):
                auth_token = user_ctrl.add_auth_token()
                self._send_reset_email(user_email, auth_token)
                message = 'Check your email to reset your pasword'
        return NtssViews().forgot_password(user_email, message)
    
    def _send_reset_email(self, email: str, auth_token: str):
        """
        Sends an email to reset the password
        """
        # Create a text/plain message
        email_content = 'Use this link to reset your password\n'
        email_content += f'{SITE_INFO["protocol"]}{SITE_INFO["hostname"]}:{SITE_INFO["port"]}"'
        email_content += f'/reset_password?verification_code={auth_token}'
        msg = EmailMessage()
        msg.set_content(email_content)

        msg['Subject'] = 'NTSS Reset Password'
        msg['From'] = 'noreply@ntss.org'
        msg['To'] = email

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    def dashboard(self):
        """
        Load the Dashboard for a User
        """
        sid = self._get_session_id()
        session_data = self._get_session_data(sid)
        return NtssViews().dashboard(session_data)
