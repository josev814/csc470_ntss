from .views import views

class ntss_views(views):

    def login_view(self):
        """
        Load the login template
        """
        self.set_template('login.html')
        print(
            self.template.render()
        )
