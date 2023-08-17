import xlsxwriter as xl
import polars as pl
def metadata_report(metadata):
    code_df = [pl.DataFrame({"Table":["Columns"]})]
    dfs = code_df + [pl.DataFrame({table.name:[col.name for col in table.c]}) for table in metadata.tables.values()]
    df = pl.concat(dfs, how = "horizontal")
    build_xl(df, "metadata_report")

def build_xl(table, report_name, file_path=None):
    if file_path is None:
        file_path = f"{report_name}.xlsx"
    with xl.Workbook(file_path) as wb:
        table.write_excel(workbook = wb)