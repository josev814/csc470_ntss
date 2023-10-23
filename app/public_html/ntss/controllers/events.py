"""
The package to handle events
"""
from ntss.controllers.controller import BaseController
from ntss.views.events import EventViews

class EventsController(BaseController):
    """
    The controller for events
    """
    def __init__(self) -> None:
        """
        Initializes the events controller
        """
        super().__init__()
    
    def get_user_event(self, event_id):
        """
        Gets an event for a user
        """
        print(f'Call event model to get event info for {event_id}')
        event_info={
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
    # add other methods below
