"""
Package for Event Views
"""
from ntss.views.views import Views


class EventViews(Views):
    """
    Class for Event Views
    """

    def __init__(self, session_info: dict):
        super().__init__()
        self._user_session = session_info
        self._controller_type = 'events'
        self.template_vars['current_user'] = self._user_session
        self.template_vars['states'] = self.US_STATES
    
    def list(self, events: list) -> str:
        """
        List events in the system
        """
        self.template_vars['pageName'] = 'List Events'
        self.template_vars['events'] = events
        if len(events) > 0:
            self.set_template('events/events_list.html')
            return self.template.render(self.template_vars)
        self.set_template('events/no_items.html')
        self.template_vars['controller_type'] = self._controller_type
        return self.template.render(self.template_vars)

    def add(self, form_values, venues, users, errors: list) -> str:
        """
        Add an event into system
        """
        self.set_template('events/add_edit.html')
        self.template_vars['pageName'] = 'Add Event'
        self.template_vars['form_post'] = form_values
        self.template_vars['venues'] = venues
        self.template_vars['users'] = users
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)
    
    def edit(self, form_values, venues, users, errors: list) -> str:
        """
        Edits an event in the system
        """
        print('fv: ', form_values)
        self.set_template('events/add_edit.html')
        self.template_vars['pageName'] = 'Edit Event'
        self.template_vars['form_post'] = form_values
        self.template_vars['venues'] = venues
        self.template_vars['users'] = users
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)

    def view(self, event_data, venue_data, cust_data) -> str:
        """
        Shows information about an event
        """
        self.set_template('events/view.html')
        self.template_vars['pageName'] = f'Event: {event_data["name"]}'
        self.template_vars['event'] = event_data
        self.template_vars['venue'] = venue_data
        self.template_vars['customer'] = cust_data
        return self.template.render(self.template_vars)

    def not_found(self, event_guid):
        """
        Shows the not found page if the event doesn't exist
        """
        self.set_template('events/not_found.html')
        self.template_vars['pageName'] = 'Event Not Found'
        self.template_vars['guid'] = event_guid
        return self.template.render(self.template_vars)

    
    def user_event(self, event_info):
        """
        Load the events for a user
        """
        self.set_template('event_info.html')
        self.template_vars['event'] = event_info
        return self.template.render(self.template_vars)

    def user_events(self):
        """
        Load the events for a user
        """
        self.set_template('events_list.html')
        self.template_vars['pageName'] = 'Events'
        return self.template.render(self.template_vars)

    def display_invoice(self, invoice_information):
        """
        Load the invoice for a user
        """
        self.set_template('print_invoice.html')
        self.template_vars['invoice_information'] = invoice_information
        return self.template.render(self.template_vars)
