"""
The NTSS package is the main controller that users access when first accessing the site.
"""
"""
The NTSS package is the main controller that users access when first accessing the site.
"""
from ntss.controllers.controller import BaseController
from ntss.views.ntss import NtssViews

class NtssController(BaseController):
    """
    The NTSS controller is the default controller that is accessed
    """
    def login(self, request_data):
        """
        Display the login page
        """
        email = None
        password = None
        if request_data.method == 'POST':
            for request_name, request_value in request_data.params.items():
                match request_name:
                    case 'email':
                        email = request_value
                    case 'password':
                        password = request_value
        return NtssViews().login_view(email, password)

    def dashboard(self):
        """
        Load the Dashboard for a User
        """
        """
        Load the Dashboard for a User
        """
        return NtssViews().dashboard()
