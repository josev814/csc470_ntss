"""
Base package for accessing the database(s)
"""
from os import getenv
from sqlalchemy import create_engine, MetaData, Table, and_


class MysqlDatabase:
    """
    The MySQL Datbase class
    """

    def __init__(self, debug=False):
        db_userpass = f"{getenv('MYSQL_USER')}:{getenv('MYSQL_PWD')}"
        db_port = getenv('MYSQL_PORT') if getenv('MYSQL_PORT') else 3306
        db_host = getenv('MYSQL_HOST')
        self._engine = create_engine(
            f"mysql://{db_userpass}@{db_host}:{db_port}",
            echo=debug
        )
        self._query = ''
        self._table = None
        self._table_name = None
        self.metadata = None

    def set_table_metadata(self):
        """
        Set the table metadata holder
        """
        self.metadata = MetaData()

    def set_table(self, table_name, auto_load: bool = True):
        """
        Setting the table that we're going to query
        """
        self._table_name = table_name
        if auto_load:
            self._table = Table(
                self._table_name, self.metadata,
                autoload_with=self._engine,
                schema=getenv('MYSQL_DATABASE')
            )
        else:
            self._table = Table(self._table_name, self.metadata, schema=getenv('MYSQL_DATABASE'))

    def db_create(self, kwdict: dict):
        """
        Method to create a record
        """
        insert_query = self._table.insert()
        with self._engine.connect() as db_conn:
            db_exec = db_conn.execute(insert_query, kwdict)
            db_conn.commit()
        return db_exec

    def db_select(self, columns: list = None, filters=None, start: int=0, limit: int = 25):
        """
        Method to select data from the database
        """
        records = []
        self._query = self._table.select()
        if filters:
            combined_filter = self.__build_query_filter(filters)
            self._query = self._query.where(combined_filter)
        
        self._query = self._query.limit(limit).offset(start)
        table_columns = self._table.columns.keys()
        with self._engine.connect() as db_conn:
            db_exec = db_conn.execute(self._query)
            try:
                for row in db_exec.fetchall():
                    row_dict = self.__create_dict_rows(row, table_columns, columns)
                    records.append(row_dict)
            except TypeError as error:
                print(f'TypeError: {error}')
        return records

    def __build_query_filter(self, filters=None):
        """
        Sets the query filter
        """
        query_filters = []
        for query_filter in filters:
            column_name = query_filter['column']
            value = query_filter['value']
            match query_filter['operator']:
                case '=':
                    filter_condition = self._table.c[column_name] == value
                case '!=':
                    filter_condition = self._table.c[column_name] != value

            query_filters.append(filter_condition)
        combined_filter = and_(*query_filters)
        return combined_filter

    def __create_dict_rows(self, row, table_columns, return_columns):
        """
        Takes the row response and builds a dictionary with column names
        """
        row_dict = {}
        for i, value in enumerate(row):
            if return_columns and table_columns[i] not in return_columns:
                continue
            row_dict[table_columns[i]] = value
        return row_dict

    def db_update(self, values: dict, filters: dict) -> int:
        """
        Method to update a record in the database
        """
        combined_filter = self.__build_query_filter(filters)
        self._query = self._table.update().where(combined_filter).values(values)
        return self.__commit_query()

    def db_delete(self, filters: dict) -> int:
        """
        Method to delete a record in the database
        """
        combined_filter = self.__build_query_filter(filters)
        self._query = self._table.delete().where(combined_filter)
        return self.__commit_query
    
    def __commit_query(self) -> int:
        with self._engine.connect() as db_conn:
            result = db_conn.execute(self._query)
            db_conn.commit()
        return result.rowcount
