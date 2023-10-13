from .views import Views

class NtssViews(Views):
    
    def login_view(self):
        """
        Load the login template
        """
        self.set_template('login.html')
        self.templateVars['pageName'] = 'Login'
        return self.template.render(self.templateVars)
    
    def dashboard(self):
        """
        Load the dashboard template
        """
        self.set_template('dashboard.html')
        self.templateVars['pageName'] = 'Dashboard'
        return self.template.render(self.templateVars)