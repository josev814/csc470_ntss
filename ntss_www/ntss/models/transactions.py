"""
This package handles interactions with the database pertaining to users
"""
from ntss.models.database import MysqlDatabase


class Transaction(MysqlDatabase):
    """
    The Transaction class that interacts with the database
    """

    def __init__(self, debug=False):
        """
        When initializing the Users model set the default table to users
        """
        super().__init__(debug)
        self.set_table_metadata()
        self.set_table('transactions')

    def get_transactions(self, columns: list=None, start: int=0, limit: int=20) -> list:
        """
        Gets all transactions from the database 
        """
        if columns:
            return self.db_select(columns, start=start, limit=limit)
        return self.db_select(start=start, limit=limit)

    def get_transaction(self, guid: str) -> dict:
        """
        Retrieves a transaction from the database based on the transaction guid
        """
        records = self.get_transactions_by_filter([{
            'column': 'transaction_guid', 'operator': '=', 'value': guid
        }], 500)
        return records[0]

    def get_transactions_by_filter(self, filters: list, limit: int=1):
        """
        Performs a select query based on the filter passed
        """
        records = self.db_select(
            filters=filters,
            limit=limit
        )
        return records
    
    def add(self, *args) -> str|bool:
        """
        Adds a transaction and returns the transaction_guid from the database
        """
        if len(args) == 1:
            args = args[0]
        else:
            raise IndexError('Too many indexes in the Tuple')

        guid = self.generate_guid()
        item_desc = args.get('item_description')
        if '#' in item_desc:
            item_desc = f'Booth: {item_desc}'
        values = {
            'transaction_guid': guid,
            'user_guid': args.get('user_guid'),
            'event_guid': args.get('event_guid'),
            'item_description': item_desc,
            'price': args.get('cost'),
            'type': args.get('transaction_type')
        }
        if self.db_create(values):
            return guid
        return False
