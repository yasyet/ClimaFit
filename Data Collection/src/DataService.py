# Author: Yasin Holzenkämpfer
# Last Modified: 23-12-2025
#
# Description: This module provides data services for the application.

import sqlite3 as sq

class DataService:
    def __init__(self, db_path):
        self.connection = sq.connect(db_path)
        self.cursonr = self.connection.cursor()
