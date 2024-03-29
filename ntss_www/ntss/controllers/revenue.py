"""
Package to handle Revenue Reports
"""
from datetime import datetime
from ntss.controllers.controller import BaseController
from ntss.models.event import Event as EventModel
from ntss.models.venue import Venue as VenueModel
from ntss.views.revenue import RevenueViews


class RevenueController(BaseController):
    """
    This class handles anything pertaining to revenue reports
    """

    def get_report(self, event_guid: str):
        """
        Gets revenue report associated with event
        """
        filters = [{'column': 'event_guid', 'operator': '=', 'value': event_guid}]
 
        joins = [{'table': 'transactions',
                  'src_column': 'event_guid', 'join_column': 'event_guid'}]
        db_event_data = EventModel(True).get_events(filters=filters, joins=joins, limit=10000)
        if len(db_event_data) == 0:
            db_event_data = EventModel(True).get_events(filters=filters)

        venue = VenueModel().get_venue_by(guid=db_event_data[0]['venue_guid'])[0]
        venue_cost = float(venue['cost'])
        print(venue)
        current_date = datetime.now()
        date = current_date.date()
        event_name = db_event_data[0]['name']
        event_id = db_event_data[0]['event_guid']
        all_transactions = db_event_data
        total_transactions = len(db_event_data)
        revenue = 0.00
        for event_data in db_event_data:
            if 'type' in event_data and event_data['type'] in ('payment','invoice'):
                revenue += float(event_data['price'])
        revenue = revenue - venue_cost
        return RevenueViews(self._session_data).get_report(date, event_name, event_id,
        all_transactions,total_transactions,revenue, venue_cost, venue)
