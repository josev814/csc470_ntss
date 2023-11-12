"""
Package for NTSS Views
"""
from ntss.views.views import Views


class NtssViews(Views):
    """
    Class for NTSS Views
    """
    def login_view(self, email=None, password=None, errors=None):
        """
        Load the login template
        """
        self.set_template('login.html')
        self.template_vars['pageName'] = 'Login'
        if email:
            self.template_vars['email'] = email
        if password:
            self.template_vars['password'] = password
        if errors:
            self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)
    
    def forgot_password(self, email=None, message=None):
        """
        Load the template for forgot password
        """
        self.set_template('forgot_password.html')
        self.template_vars['pageName'] = 'Forgot Password'
        if email:
            self.template_vars['email'] = email
        if message:
            self.template_vars['message'] = message
        return self.template.render(self.template_vars)

    def dashboard(self, user_info):
        """
        Load the dashboard template
        """
        self.set_template('dashboard.html')
        self.template_vars['pageName'] = 'Dashboard'
        self.template_vars['user'] = user_info
        return self.template.render(self.template_vars)
