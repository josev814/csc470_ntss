"""
Package for User Views
"""
from ntss.views.views import Views


class VenueViews(Views):
    """
    The class for handling views for venues
    """
    
    def __init__(self, session_info: dict):
        super().__init__()
        self._user_session = session_info
        self._controller_type = 'venues'

    def get_venue(self, venue_info) -> str:
        """
        Load the venue page
        """
        self.set_template('venues/profile.html')
        self.template_vars['states'] = self.US_STATES
        self.template_vars['venue'] = venue_info
        self.template_vars['current_user'] = self._user_session
        return self.template.render(self.template_vars)
    
    def add(self, form_values, errors: list) -> str:
        """
        Add a venue into system
        """
        self.set_template('venues/add.html')
        self.template_vars['pageName'] = 'Add Venue'
        self.template_vars['states'] = self.US_STATES
        self.template_vars['current_user'] = self._user_session
        self.template_vars['form_post'] = form_values
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)
    
    def list(self, venues: list) -> str:
        """
        List venues in the system
        """
        self.template_vars['pageName'] = 'List Venues'
        self.template_vars['current_user'] = self._user_session
        self.template_vars['venues'] = venues
        if len(venues) > 0:
            self.set_template('venues/list.html')
            return self.template.render(self.template_vars)
        self.set_template('venues/no_items.html')
        self.template_vars['controller_type'] = self._controller_type
        return self.template.render(self.template_vars)
