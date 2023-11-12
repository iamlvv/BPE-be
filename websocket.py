import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")

conn.cursor().execute("LISTEN test;")
