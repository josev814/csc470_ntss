"""
This package handles interactions with the database pertaining to users
"""
from ntss.models.database import MysqlDatabase

class RevenueModel(MysqlDatabase):
    """
    Revenue class that interacts with the database
    """

    # def __init__(self, debug=False):
    #     """
    #     When initializing the Users model set the default table to users
    #     """
    #     super().__init__(debug)
    #     self.set_table_metadata()
    #     self.set_table('revenues')

