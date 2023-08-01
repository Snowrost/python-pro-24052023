import psycopg


def list_big_table(number: int) -> list:
    with psycopg.connect("dbname=dealership user=dealership password=password") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM big_table as bt JOIN another_big_table as abt ON bt.id = abt.big_table_id "
            "WHERE bt.number <= %(number)s",
            {"number": number},
        )
        return cursor.fetchall()
