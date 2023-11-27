"""
Package to handle Users
"""
from ntss.controllers.controller import BaseController
from ntss.views.events import EventViews
from ntss.models.event import Event as EventModel, EventUsers as EventUsersModel
from ntss.models.venue import Venue as VenueModel
from ntss.models.user import Users as UsersModel
from ntss.models.transactions import Transaction as TransactionModel
from ntss.views.revenue import RevenueViews
from datetime import datetime


class RevenueController(BaseController):
    """
    This class handles anything pertaining to revenue reports
    """

    def get_report(self, event_guid: str):
        """
        Gets revenue report associated with event
        """
        columns = ['event_guid', 'event_name', 'transactions', 'name', ]
        joins = [{'table': 'transactions',
                  'src_column': 'event_guid', 'join_column': 'event_guid'}]
        db_event_data = EventModel(True).get_events(joins=joins, limit=10000)
        venue = VenueModel().get_venue_by(guid=db_event_data[0]['venue_guid'])[0]
        venue_cost = float(venue['cost'])
        print(venue)
        current_date = datetime.now()
        date = current_date.date()
        eventName = db_event_data[0]['name']
        eventId = db_event_data[0]['event_guid']
        all_transactions = db_event_data
        total_transactions = len(db_event_data)
        revenue = 0.00
        for event_data in db_event_data:
            if event_data['type'] in ('payment','invoice'):
                revenue += float(event_data['price'])
                print(float(event_data['price']))
        revenue = revenue - venue_cost
        return RevenueViews(self._session_data).get_report(date, eventName, eventId, all_transactions,total_transactions,revenue, venue_cost, venue)
