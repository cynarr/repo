def flush_rows(schema, conn, rows):
    import pandas
    df = pandas.DataFrame(rows)
    conn.register('df', df)
    conn.execute(f"INSERT INTO {schema} SELECT * FROM df;")
    conn.unregister('df')
    rows.clear()
    conn.commit()
