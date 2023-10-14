from ntss.views.ntss import NtssViews

class NtssController():

    def __init__(self) -> None:
        if not self.is_logged_in() and not self.get_permissions():
            # redirect to home to login
            pass
        if not self.has_access():
            # load a view for access denied
            pass

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
        return NtssViews().dashboard()
    
    def is_logged_in(self):
        return False

    def get_permissions(self):
        return False
    
    def has_access(self):
        return False