"""
This package handles interactions with the database pertaining to users
"""
from ntss.models.database import MysqlDatabase


class Event(MysqlDatabase):
    """
    The Event class that interacts with the database
    """

    def __init__(self, debug=False):
        """
        When initializing the Users model set the default table to users
        """
        super().__init__(debug)
        self.set_table_metadata()
        self.set_table('events')

    def get_events(self, columns: list=None, joins: list=None, start: int=0, limit: int=20) -> list:
        """
        Gets all events from the database 
        """
        if columns and joins:
            return self.db_select(columns=columns, joins=joins, start=start, limit=limit)
        if joins:
            return self.db_select(joins=joins, start=start, limit=limit)
        if columns:
            return self.db_select(columns, start=start, limit=limit)
        return self.db_select(start=start, limit=limit)

    def get_event(self, guid: str) -> dict:
        """
        Retrieves a event from the database based on the event guid
        """
        records = self.get_event_by(guid=guid)
        return records[0]

    def get_event_by(self, name=None, city=None, state=None, guid=None, user_guid = None, limit: int=1):
        """
        Performs a select query based on the params passed
        """
        query_filter = []
        if guid:
            query_filter.append(
                {'column': 'event_guid', 'operator': '=', 'value': guid}
            )
        if name:
            query_filter.append(
                {'column': 'name', 'operator': '=', 'value': name}
            )
        if city:
            query_filter.append(
                {'column': 'city', 'operator': '=', 'value': city}
            )
        if state:
            query_filter.append(
                {'column': 'state', 'operator': '=', 'value': state}
            )
        if user_guid:
            query_filter.append(
                {'column': 'user_guid', 'operator': '=', 'value': user_guid}
            )
        records = self.db_select(
            filters=query_filter,
            limit=limit
        )
        return records
    
    def add(self, *args) -> str|bool:
        """
        Adds a event and returns the event_guid from the database
        """
        if len(args) == 1:
            args = args[0]
        else:
            raise IndexError('Too many indexes in the Tuple')

        guid = self.generate_guid()
        values = {
            'event_guid': guid,
            'venue_guid': args.get('venue_guid'),
            'user_guid': args.get('user_guid'),
            'name': args.get('name'),
            'theme': args.get('theme'),
            'booths': args.get('booths'),
            'conference_rooms': args.get('conference_rooms'),
            'start_date': args.get('start_date'),
            'end_date': args.get('end_date'),
            'website': args.get('website')
        }
        if self.db_create(values):
            return guid
        return False

    def update(self, guid, *args) -> str|bool:
        """
        Updates a event based on its guid
        """
        if len(args) == 1:
            args = args[0]
        else:
            raise IndexError('Too many indexes in the Tuple')
        
        values = {
            'venue_guid': args.get('venue_guid'),
            'user_guid': args.get('user_guid'),
            'name': args.get('name'),
            'booths': args.get('booths'),
            'conference_rooms': args.get('conference_rooms'),
            'website': args.get('website'),
            'theme': args.get('theme'),
            'start_date': args.get('start_date'),
            'end_date': args.get('end_date'),
        }
        filters = [
            {'column': 'event_guid', 'operator': '=', 'value': f'{guid}'}
        ]

        return bool(self.db_update(values, filters))

    def delete(self, guid):
        """
        Deletes a event from the database
        """
        filters = [
            {'column': 'event_guid', 'operator': '=', 'value': f'{guid}'}
        ]
        return self.db_delete(filters)
