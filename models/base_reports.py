def metadata_report(metadata):
    for table in metadata.tables.values():
        print(f"{table}")
        print(f"    {table.c}")