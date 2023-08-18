from cmd import Cmd
from typing import IO
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import pandas as pd
from tabulate import tabulate
from shutil import get_terminal_size
import re

pd.set_option('display.width', get_terminal_size()[0])

class Dbr(Cmd):
    def __init__(self, engine):
        self._engine = engine
        self.metadata = self._engine._base.metadata
        self.tables = self.metadata.tables
        self.filter_options = [">", ">=", "<", "<=", "=", "!=", "like"]
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
        table = self.get_value("What table would you like to access? Enter q to exit.\n", self.tables)[0]
        if table:
            primary_keys = [c.name.lower() for c in self.tables[table].primary_key]
            table_cols = [c.name.lower() for c in self.tables[table].c if c.name.lower() not in primary_keys]
            columns = self.get_value(f"What columns would you like to select?\nOptions: {table_cols}. Enter for all.\n", table_cols)
            if not columns:
                columns = table_cols
            filters = []
            print(f"""Would you like to filter any of {columns}?
    Options: {self.filter_options}
    Syntax: column filter value
    Use column filter value [AND/OR] [NOT] column filter value ... to have dual+ condition, otherwise all conditions will be treated as all needing to be true.
    Enter to skip.\n""")
            while True:
                filter = input()
                if filter != "":
                    if filter.startswith('(') and filter.endswith(')'):
                        filters.append([filter])
                    else:
                        multi_check = re.split(r"( and | or )", filter)
                        if len(multi_check) > 1:
                            filters += [clause.strip().lower().split(" ") for clause in multi_check]
                        else:
                            given = filter.lower().split(" ")
                            filters.append(given)
                else:
                    break
            # print(filters)
            query = self.build_sql_query(table, columns, filters)
            # print(query)
            self.write_excel(query, table)
            
        else:
            print("That is not an accepted table name. Please try again.\n")
            self.do_get_tables()
            self.do_query_builder()

    def get_value(self, request_str, options):
        val = input(request_str)
        if val == "q" or val == "":
            return
        val = val.split(" ")
        check, val = _asserter(val, options)
        if check:
            return val
        else:
            print(f"That choice is not one of the supported options: {options}")
            self.get_value(request_str, options)


    def build_sql_query(self, table, columns, filters):
        stmt = f"""SELECT {", ".join(columns)} FROM {table}"""
        if filters != []:
            filter_stmt = ""
            for filter in filters:
                if filter[0].startswith("(") and filter[0].endswith(")"):
                    filter_stmt = filter_stmt.rstrip(" AND ") + f"{filter[0]} AND "
                    continue
                if (filter == ['and'] or filter == ['or']):
                    filter_stmt = filter_stmt.rstrip(" AND ") + f" {filter[0]} "
                    continue
                else:
                    if filter[0] == 'not':
                        filter_stmt += ' not '
                        filter.pop(0)
                    col_exists, val = _asserter([filter[0]], columns)
                    if col_exists:
                        filter_option_exists, val = _asserter([filter[1]], self.filter_options)
                        if filter_option_exists:
                            filter_stmt += f"""{' '.join(filter)} AND """
                        else:
                            print(f"{filter[1]} is not a valid filter, skipping filter of {filter[0]}")
                            continue
                    else:
                        print(f"Did not select {filter[0]} as column, skipping filtering")
                        continue
            filter_stmt = filter_stmt.lower()
            filter_stmt = filter_stmt.rstrip(" ")
            filter_stmt = filter_stmt.rstrip("and")
            filter_stmt = filter_stmt.rstrip("or")
            filter_stmt = filter_stmt.rstrip("not")
            stmt = stmt if filter_stmt == "" else stmt + " WHERE " + filter_stmt
            stmt = stmt.strip("WHERE ")
        return stmt.rstrip(", ")

    def do_put(self):
        pass

    def do_get_report(self):
        pass

    def do_edit_report(self):
        pass

    def write_excel(self, query, report_name):
        with self._engine._engine.connect() as con:
            res = pd.read_sql(query, con=con)
            res.to_excel(f"reports/{report_name}.xlsx")

def _asserter(value, supposed_to):
    try:
        assert all([val in supposed_to for val in value])
        return True, value
    except AssertionError:
        if any([val in supposed_to for val in value]):
            print(f"Options {[val for val in value if val not in supposed_to]} are not valid options")
            return True, [val for val in value if val in supposed_to]
        return False, None

def run_cli_loop(engine):
    dbr = Dbr(engine=engine)
    dbr.prompt = "dbr > "
    dbr.cmdloop()

