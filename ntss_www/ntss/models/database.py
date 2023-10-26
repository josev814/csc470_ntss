"""
Base package for accessing the database(s)
"""
from os import getenv
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session


class MysqlDatabase:
    """
    The MySQL Datbase class
    """
    table = None

    def __init__(self):
        db_userpass = f"{getenv('db_user')}:{getenv('db_pass')}"
        self._engine = create_engine(
            f"mysql://{db_userpass}@{getenv('db_host')}:{getenv('db_port')}",
            echo=True
        )
        self._query = ''

    def create(self, kwdict):
        """
        Method to create a record
        """

    def select(self, columns, filters=None):
        """
        Method to select data from the database
        """
        records = []
        self._query = select(self.table.c['","'.join(columns)])
        for query_filter in filters:
            if query_filter.operator == '=':
                self._query.where(f'{query_filter.column}' == f'{query_filter.value}')

        with Session(self._engine) as db_sess:
            for row in db_sess.execute(self._query):
                records.append(row)
        return records

    def update(self):
        """
        Method to update a record in the database
        """

    def delete(self):
        """
        Method to delete a record in the database
        """
