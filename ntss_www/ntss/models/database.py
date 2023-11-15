"""
Base package for accessing the database(s)
"""
from os import getenv
from uuid import uuid4
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
        self._join_table = None
        self._table_name = None
        self._join_table_name = None
        self.metadata = None
        self.join_metadata = None

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
    
    def set_join_table(self, table_name, auto_load: bool = True):
        """
        Setting the table that we're going to join with
        """
        self._join_table_name = table_name
        if auto_load:
            self._join_table = Table(
                self._join_table_name, MetaData(),
                autoload_with=self._engine,
                schema=getenv('MYSQL_DATABASE')
            )
        else:
            self._join_table = Table(self._join_table_name, MetaData(), schema=getenv('MYSQL_DATABASE'))

    def db_create(self, kwdict: dict):
        """
        Method to create a record
        """
        insert_query = self._table.insert()
        with self._engine.connect() as db_conn:
            db_exec = db_conn.execute(insert_query, kwdict)
            db_conn.commit()
        return db_exec

    def db_select(self, columns: list = None, joins: list = None, filters=None, start: int=0, limit: int = 25):
        """
        Method to select data from the database
        """
        records = []
        if joins:
            for join in joins:
                self.set_join_table(join['table'])
                self._query = self._table.select().add_columns(self._join_table.c)
                self._query.join_from(self._table, self._join_table, self._table.c[join['src_column']] == self._join_table.c[join['join_column']])
        else:
            self._query = self._table.select()
        if filters:
            combined_filter = self.__build_query_filter(filters)
            self._query = self._query.where(combined_filter)
        
        self._query = self._query.limit(limit).offset(start)
        with self._engine.connect() as db_conn:
            try:
                db_exec = db_conn.execute(self._query)
                for row in db_exec.fetchall():
                    row_dict = self.__create_dict_rows(row, columns, self._query.exported_columns)
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

    def __create_dict_rows(self, row, return_columns, table_columns):
        """
        Takes the row response and builds a dictionary with column names
        """
        row_dict = {}
        table_columns = [str(exported_column) for exported_column in self._query.exported_columns.keys()]
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
        return self.__commit_query()
    
    def __commit_query(self) -> int:
        with self._engine.connect() as db_conn:
            result = db_conn.execute(self._query)
            db_conn.commit()
        return result.rowcount

    @staticmethod
    def generate_guid() -> str:
        """
        Generates a hex unique identifier
        :return: str
        """
        return uuid4().hex
