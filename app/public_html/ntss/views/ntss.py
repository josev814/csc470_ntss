from .views import Views

class NtssViews(Views):

    def login_view(self):
        """
        Load the login template
        """
        self.set_template('login.html')
        print(
            self.template.render()
        )
