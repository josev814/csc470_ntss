"""
Package for User Views
"""
from ntss.views.views import Views


class UserViews(Views):
    """
    The class for handling views for users
    """

    def get_user_profile(self, user_info):
        """
        Load the the profile for a user
        """
        self.set_template('user_profile.html')
        self.template_vars['user'] = user_info
        return self.template.render(self.template_vars)
    
    def add_user(self):
        """
        Add a user into system
        """
        self.set_template('add_user.html')
        self.template_vars['pageName'] = 'Add User'
        self.template_vars['states'] = self.US_STATES
        return self.template.render(self.template_vars)
