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

    def do_query_builder(self, *a, **k):
        """Build query for report"""
        table = input("What table would you like to access?\n")
        table_check = _asserter([table], self.tables)
        if table_check:
            primary_keys = [c.name.lower() for c in self.tables[table].primary_key]
            table_cols = [c.name.lower() for c in self.tables[table].c if c.name.lower() not in primary_keys]
            columns = input(f"What columns would you like to select?\nEnter * for all. \nOptions: {table_cols}\n")
            columns = [col for col in columns.split(" ")]
            if columns == ["*"]:
                columns = table_cols
            col_check = _asserter(columns, table_cols)
            if col_check:
                filters = []
                self.filter_options = [">", ">=", "<", "<=", "=", "!=", "like"]
                print(f"Would you like to filter any of {columns}?\n")
                print(f"Options: {self.filter_options}\nSyntax: column filter value\n")
                while True:
                    filter = input()
                    if filter != "":
                        given = filter.split(" ")
                        filters.append(given)
                    else:
                        break
                query = self.build_sql_query(table, columns, filters)
                with self._engine._engine.connect() as con:
                    res = pd.read_sql(query, con=con)
                    print(res)
            else:
                print("Those are not all valid columns.")
                print(table_cols)

        else:
            print("That is not an accepted table name. Please try again.\n")
            self.do_get_tables()
            self.do_query_builder()

    def build_sql_query(self, table, columns, filters):
        stmt = f"""SELECT {", ".join(columns)} FROM {table}"""
        if filters != []:
            stmt += " WHERE "
            for filter in filters:
                col_exists = _asserter([filter[0]], columns)
                if col_exists:
                    filter_option_exists = _asserter([filter[1]], self.filter_options)
                    if filter_option_exists:
                        filter_stmt = f"""{' '.join(filter)}, """
                        stmt += filter_stmt
                    else:
                        print(f"{filter[1]} is not a valid filter, skipping filter of {filter[0]}")
                        continue
                else:
                    print(f"Did not select {filter[0]} as column, skipping filtering")
                    continue
        stmt.strip("WHERE")
        return stmt.rstrip(", ")

            
        


    def do_put(self):
        pass

    def do_get_report(self):
        pass

    def do_edit_report(self):
        pass

def _asserter(value, supposed_to):
    try:
        assert all([val in supposed_to for val in value])
        return True
    except AssertionError:
        return False


def run_cli_loop(engine):
    dbr = Dbr(engine=engine)
    dbr.prompt = "dbr > "
    dbr.cmdloop()

