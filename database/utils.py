def flush_rows(schema, conn, rows):
    import pandas
    df = pandas.DataFrame(rows)
    conn.register('df', df)
    conn.execute(f"INSERT INTO {schema} SELECT * FROM df;")
    conn.unregister('df')
    rows.clear()
    conn.commit()


def get_doc_id_map(conn):
    doc_url_pairs = conn.execute(
        "SELECT document_id, canon_url FROM documents"
    ).fetchnumpy()
    return dict(zip(doc_url_pairs["canon_url"], doc_url_pairs["document_id"]))
