"""
The package to handle events
"""
from ntss.controllers.controller import BaseController
from ntss.views.events import EventViews
from ntss.models.event import Event as EventModel
from ntss.models.venue import Venue as VenueModel
from ntss.models.user import Users as UsersModel


class EventsController(BaseController):
    """
    The controller for events
    """

    def list(self, start: int=0):
        """
        Lists the events in the system
        """
        columns = ['event_guid', 'name', 'name_1', 'city', 'state', 'start_date', 'end_date']
        joins = [{'table': 'venues', 'src_column': 'venue_guid', 'join_column': 'venue_guid'}]
        db_event_data = EventModel(True).get_events(columns=columns, joins=joins, start=start)
        event_data = []
        for db_event in db_event_data:
            venue_name = db_event['name_1']
            db_event['venue'] = venue_name
            del db_event['name_1']
            event_data.append(db_event)
        return EventViews(self._session_data).list(event_data)

    def add(self):
        """
        Adds an event into the system
        """
        posted_values = {}
        errors = None
        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                posted_values[request_name] = request_value.strip()
            is_valid, errors = self.__verify_add_form(posted_values)
            if is_valid:
                venue_guid = EventModel().add(
                    posted_values
                )
                if venue_guid:
                    return self.redirect('/events/list')
        venues = VenueModel().get_venues(['venue_guid', 'name', 'booths', 'conference_rooms'])
        users = UsersModel().get_users(['user_guid', 'first_name', 'last_name'])
        return EventViews(self._session_data).add(posted_values, venues, users, errors)
    
    def edit(self, event_guid):
        """
        Adds an event into the system
        """
        posted_values = {}
        errors = None
        event_info = EventModel().get_event_by(guid=event_guid)
        if len(event_info) == 0:
            return EventViews(self._session_data).not_found(event_guid)
        event_info = event_info[0]
        
        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                posted_values[request_name] = request_value.strip()
            event_info = posted_values
            is_valid, errors = self.__verify_edit_form(posted_values)
            if is_valid and EventModel().update(event_guid, posted_values):
                errors.append('Event was successfully Updated')
        venues = VenueModel().get_venues(['venue_guid', 'name', 'booths', 'conference_rooms'])
        users = UsersModel().get_users(['user_guid', 'first_name', 'last_name'])
        return EventViews(self._session_data).edit(event_info, venues, users, errors)

    def view_event(self, event_guid):
        event_info = EventModel().get_event_by(guid=event_guid)
        if len(event_info) == 0:
            return EventViews(self._session_data).not_found(event_guid)
        event_info = event_info[0]
        venue_info = VenueModel().get_venue_by(guid=event_info['venue_guid'])[0]
        owner_info = UsersModel().get_user_by(user_guid=event_info['user_guid'])[0]
        return EventViews(self._session_data).view(event_info, venue_info, owner_info)
    
    def delete(self, guid):
        """
        Delete a venue
        """
        try:
            event_data = EventModel().get_event_by(guid=guid)
            if len(event_data) == 0:
                raise Exception
            if not EventModel().delete(guid):
                raise Exception
            return self.redirect('/events/list')
        except:
            return EventViews(self._session_data).not_found(guid)

    def __verify_add_form(self, posted_values):
        """
        Verifies that we have all the data for the add event form
        """
        errors = []
        is_valid = True
        if(posted_values.get('venue_guid') == ''):
            errors.append('You must select a venue')
            # TODO: Add more validations for this form
            # are we trying to reserve a venue that doesn't have enough booths or rooms?
        if len(errors) > 0:
            is_valid = False
        return is_valid, errors
    
    def __verify_edit_form(self, posted_values):
        """
        Verifies that we have all the data for the edit event form
        """
        errors = []
        is_valid = True
        if(posted_values.get('venue_guid') == ''):
            errors.append('You must select a venue')
        if(posted_values.get('user_guid') == ''):
            errors.append('You must select an owner')
            # TODO: Add more validations for this form
            # are we trying to reserve a venue that doesn't have enough booths or rooms?
        if len(errors) > 0:
            is_valid = False
        return is_valid, errors
    

    def get_user_event(self, event_id):
        """
        Gets an event for a user
        """
        print(f'Call event model to get event info for {event_id}')
        event_info = {
            'id': 12,
            'name': "Event XII",
            'description': '',
            'booths': 3,
            'start_date': 'Oct 23, 2023',
            'end_date': 'Oct 31, 2023',
            'location': 'Fayetteville, NC',
            'venue': 'Fayetteville State University'
        }
        return EventViews().user_event(event_info)

    def get_user_events(self):
        """
        Gets events that is associated with a user
        """
        return EventViews().user_events()

    def get_exhibitor_booth_invoice(self, event_id, invoice_id):
        """
        Gets an event for a user
        """
        event_info = {
            'id': event_id,
            'name': "Event XII",
            'description': '',
            'booths': 3,
            'start_date': 'Oct 23, 2023',
            'end_date': 'Oct 31, 2023',
            'location': 'Fayetteville, NC',
            'venue': 'Fayetteville State University'
        }
        customer_info = {
            'id': 345,
            'name': 'Jose\' Vargas',
            'address': '1234 Pelican Bay',
            'city': 'New York City',
            'state': 'New York',
            'zipcode': 1001
        }
        invoice_items = [{
            'name': 'Booth Reservation',
            'qty': event_info['booths'],
            'price': 45,
            'subtotal': (event_info['booths'] * 45)
        }]
        tax = 0
        subtotal = sum(item['subtotal'] for item in invoice_items)
        invoice_details = {
            'items': invoice_items,
            'total': round(subtotal * tax + subtotal, 2),
            'subtotal': subtotal,
            'tax': tax
        }
        invoice_information = {
            'id': invoice_id,
            'date': 'Oct 20, 2023',
            'event': event_info,
            'customer': customer_info,
            'invoice_details': invoice_details
        }
        return EventViews().display_invoice(invoice_information)
    # add other methods below
