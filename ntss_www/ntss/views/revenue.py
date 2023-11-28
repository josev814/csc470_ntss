"""
Package for Revenue Views
"""
from ntss.views.views import Views

class RevenueViews(Views):
    """
    The class for handling revenue reports for users by admin/staff
    """

    def __init__(self, session_info: dict):
        super().__init__()
        self._user_session = session_info
        self._controller_type = 'revenue'
        self.template_vars['current_user'] = self._user_session


    def get_report(self, date, event_name, event_id, all_transactions,
            total_transactions, revenue, venue_cost, venue):
        """
        Get revenue report
        """
        self.set_template('revenue_report.html')
        self.template_vars['pageName'] = 'Revenue Report'
        self.template_vars['date'] = date
        self.template_vars['eventName'] = event_name
        self.template_vars['eventId'] = event_id
        self.template_vars['totalTransactions'] = total_transactions
        self.template_vars['allTransactions'] = all_transactions
        self.template_vars['venueCost'] = venue_cost 
        self.template_vars['venue'] = venue
        self.template_vars['totalRevenue'] = f'{revenue:.2f}'
        return self.template.render(self.template_vars)
