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
        self.templateVars['pageName'] = 'Login'
        if email:
            self.templateVars['email'] = email
        if password:
            self.templateVars['password'] = password
        if errors:
            self.templateVars['errors'] = errors
        return self.template.render(self.templateVars)
    
    def forgot_password(self, email=None, message=None):
        """
        Load the template for forgot password
        """
        self.set_template('forgot_password.html')
        self.templateVars['pageName'] = 'Forgot Password'
        if email:
            self.templateVars['email'] = email
        if message:
            self.templateVars['message'] = message
        return self.template.render(self.templateVars)

    def dashboard(self):
        """
        Load the dashboard template
        """
        self.set_template('dashboard.html')
        self.templateVars['pageName'] = 'Dashboard'
        return self.template.render(self.templateVars)
