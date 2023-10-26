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
        self.templateVars['user'] = user_info
        self.templateVars['pageName'] = 'User Profile'
        return self.template.render(self.templateVars)
