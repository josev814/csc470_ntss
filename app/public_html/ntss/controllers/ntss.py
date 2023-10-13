from ntss.views.ntss import NtssViews

class NtssController():

    def __init__(self) -> None:
        if not self.is_logged_in() and not self.get_permissions():
            # redirect to home to login
            pass
        if not self.has_access():
            # load a view for access denied
            pass

    def login(self):
        return NtssViews().login_view()

    def dashboard(self):
        return NtssViews().dashboard()
    
    def is_logged_in(self):
        return False

    def get_permissions(self):
        return False
    
    def has_access(self):
        return False