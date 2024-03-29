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
        self.set_template('events/add_edit.html')
        self.template_vars['pageName'] = 'Edit Event'
        self.template_vars['form_post'] = form_values
        self.template_vars['venues'] = venues
        self.template_vars['users'] = users
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)

    def view(self, event_data, venue_data, cust_data,
        attendee_data, transactions, speech_data) -> str:
        """
        Shows information about an event
        """
        self.set_template('events/view.html')
        self.template_vars['pageName'] = f'Event: {event_data["name"]}'
        self.template_vars['event'] = event_data
        self.template_vars['venue'] = venue_data
        self.template_vars['customer'] = cust_data
        self.template_vars['attendees'] = attendee_data
        self.template_vars['trxns'] = transactions
        self.template_vars['speeches'] = speech_data
        return self.template.render(self.template_vars)
    
    def search(self, events: list, form_data: dict) -> str:
        """
        List events in the system from a search
        """
        self.template_vars['pageName'] = 'List Events'
        self.template_vars['events'] = events
        self.template_vars['form_data'] = form_data
        if len(events) > 0:
            self.set_template('events/events_list.html')
            return self.template.render(self.template_vars)
        self.set_template('events/no_items.html')
        self.template_vars['controller_type'] = self._controller_type
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

    def user_events(self, events_info):
        """
        Load the events for a user
        """

        self.template_vars['pageName'] = 'Events'
        self.template_vars['events'] = events_info
        if len(events_info) > 0:
            self.set_template('/events/user_events_list.html')
        else:
            self.set_template('events/no_items.html')
            self.template_vars['controller_type'] = self._controller_type
        return self.template.render(self.template_vars)

    def view_customer_event(self, event_data, venue_data) -> str:
        """
        View Customer Event
        """
        self.set_template('/events/customer_event_info.html')
        self.template_vars['pageName'] = f'Event: {event_data["name"]}'
        self.template_vars['event'] = event_data
        self.template_vars['venue'] = venue_data
        return self.template.render(self.template_vars)

    def display_invoice(self, invoice_information):
        """
        Load the invoice for a user
        """
        self.set_template('print_invoice.html')
        self.template_vars['invoice_information'] = invoice_information
        return self.template.render(self.template_vars)

    def form_add_attendee(self, form_data, event_info, users, reserved_boths, messages):
        """
        Load the form for adding a user to an event
        """
        self.set_template('events/add_attendee.html')
        self.template_vars['pageName'] = 'Add Attendee'
        self.template_vars['form_data'] = form_data
        self.template_vars['event'] = event_info
        self.template_vars['reserved_booths'] = reserved_boths
        self.template_vars['users'] = users
        self.template_vars['errors'] = messages
        return self.template.render(self.template_vars)
    
    def get_user_report(self, user_roles, date, event_name):
        """
        Get user reports
        """
        self.set_template('/events/get_report.html')
        self.template_vars['pageName'] = 'User Report'
        self.template_vars['event_name'] = event_name
        self.template_vars['user_roles'] = user_roles
        self.template_vars['date'] = date
        return self.template.render(self.template_vars)


class ExhibitViews(Views):
    """
    Class for Exhibit Views
    """

    def __init__(self, session_info: dict):
        super().__init__()
        self._user_session = session_info
        self.template_vars['current_user'] = self._user_session
        self._controller_type = 'exhibits'

    def list(self, exhibits: list):
        """
        List exhibits in the system
        """
        self.template_vars['pageName'] = 'List Exhibits'
        self.template_vars['exhibits'] = exhibits
        if len(exhibits) > 0:
            self.set_template('events/exhibits/list.html')
            return self.template.render(self.template_vars)
        self.template_vars['controller_type'] = self._controller_type
        self.set_template('no_items.html')
        return self.template.render(self.template_vars)
    
    def edit_exhibit(self, exhibit: dict, form_data: dict, messages: list) -> str:
        """
        Displays the form for editing an exhibit
        """
        self.template_vars['pageName'] = f'Exhibit: {exhibit["transaction_guid"]}'
        self.template_vars['exhibit'] = exhibit
        self.template_vars['form_data'] = form_data
        self.template_vars['errors'] = messages
        self.set_template('events/exhibits/edit.html')
        return self.template.render(self.template_vars)
