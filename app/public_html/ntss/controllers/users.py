from ntss.views.users import UserViews

class UsersController():

    def __init__(self) -> None:
        if not self.is_logged_in() and not self.get_permissions():
            # redirect to home to login
            pass
        if not self.has_access():
            # load a view for access denied

    # add other methods below
    # Views should be placed in the views -> users.py file
