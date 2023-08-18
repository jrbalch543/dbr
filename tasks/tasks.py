from cmd import Cmd
from typing import IO
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import pandas as pd
from tabulate import tabulate
from shutil import get_terminal_size

pd.set_option('display.width', get_terminal_size()[0])

class Dbr(Cmd):
    def __init__(self, engine):
        self._engine = engine
        self.metadata = self._engine._base.metadata
        self.tables = self.metadata.tables
        super().__init__()

    def do_q(self, *a, **k):
        exit()

    def do_get_tables(self, *a, **k):
        """Get tables from connected engine"""
        print("TABLES:")
        for _table_name in self.tables:
            print(f"    Table: {_table_name}")

    def do_get_table_head(self, table, *a, **k):
        """Get first five rows of a table"""
        if table in self.tables:
            with self._engine._engine.connect() as con:
                res = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", con=con)
                print(tabulate(res, showindex=False, headers='keys', tablefmt='psql'))
        else:
            print(f"Table {table} is not a table in the database. \nPlease select from one of the following tables:")
            self.do_get_tables()

    def do_query_builder(self):
        """Build query for report"""
        table = input("What table would you like to access?\n")
        assert table in self.tables, ValueError(f"That is not an accepted table name. Please try again.")
    

    def do_put(self):
        pass

    def do_get_report(self):
        pass

    def do_edit_report(self):
        pass


def run_cli_loop(engine):
    dbr = Dbr(engine=engine)
    dbr.prompt = "dbr > "
    dbr.cmdloop()

