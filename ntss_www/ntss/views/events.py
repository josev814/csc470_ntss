"""
Package for Event Views
"""
from ntss.views.views import Views

class EventViews(Views):
    """
    Class for Event Views
    """
    def user_event(self, event_info):
        """
        Load the events for a user
        """
        self.set_template('event_info.html')
        self.templateVars['event'] = event_info
        return self.template.render(self.templateVars)
    
    def user_events(self):
        """
        Load the events for a user
        """
        self.set_template('events_list.html')
        self.templateVars['pageName'] = 'Events'
        return self.template.render(self.templateVars)

    def display_invoice(self, invoice_information):
        """
        Load the invoice for a user
        """
        self.set_template('print_invoice.html')
        self.templateVars['invoice_information'] = invoice_information
        return self.template.render(self.templateVars)
