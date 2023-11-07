"""
Base package for accessing the database(s)
"""
from os import getenv
from sqlalchemy import create_engine, MetaData, Table, and_


class MysqlDatabase:
    """
    The MySQL Datbase class
    """

    def __init__(self):
        db_userpass = f"{getenv('MYSQL_USER')}:{getenv('MYSQL_PWD')}"
        db_port = getenv('MYSQL_PORT') if getenv('MYSQL_PORT') else 3306
        db_host = getenv('MYSQL_HOST')
        print('Connecting to', f'mysql://{db_userpass}@{db_host}:{db_port}')
        self._engine = create_engine(
            f"mysql://{db_userpass}@{db_host}:{db_port}",
            echo=True
        )
        self._query = ''
        self._table = None
        self._table_name = None
        self.metadata = None

    def set_table_metadata(self, metadata=None):
        self.metadata = MetaData()
        if metadata:
            pass

    def set_table(self, table_name, auto_load: bool = True):
        self._table_name = table_name
        print(self._table_name)
        print(getenv('MYSQL_DATABASE'))
        if auto_load:
            self._table = Table(
                self._table_name, self.metadata,
                autoload_with=self._engine,
                schema=getenv('MYSQL_DATABASE')
            )
        else:
            self._table = Table(self._table_name, self.metadata, schema=getenv('MYSQL_DATABASE'))

    def db_create(self, kwdict):
        """
        Method to create a record
        """
        insert_query = self._table.insert()
        value_list = [*kwdict]
        with self._engine.connect() as db_conn:
            db_exec = db_conn.execute(insert_query, value_list)
        return db_exec

    def db_select(self, columns: list = [], filters=None):
        """
        Method to select data from the database
        """
        records = []
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

        self._query = self._table.select().where(combined_filter)
        table_columns = self._table.columns.keys()
        with self._engine.connect() as db_conn:
            db_exec = db_conn.execute(self._query)
            if db_exec:
                try:
                    for row in db_exec.fetchmany(1):
                        row_dict = {}
                        for i in range(len(row)):
                            if columns and table_columns[i] not in columns:
                                continue
                            row_dict[table_columns[i]] = row[i]
                        records.append(row_dict)
                except TypeError as error:
                    print(f'TypeError: {error}')
        return records

    def db_update(self):
        """
        Method to update a record in the database
        """

    def db_delete(self):
        """
        Method to delete a record in the database
        """
