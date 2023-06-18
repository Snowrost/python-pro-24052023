import os

import psycopg2
from psycopg2.pool import SimpleConnectionPool


def main():
    single_connection_example()
    pooled_connection_example()


def single_connection_example():
    connection = psycopg2.connect(host="127.0.0.1",
                                  port=5432,
                                  dbname="test_database",
                                  user="test_user",
                                  password=os.environ.get("DB_PASSWORD", "password"))
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    print("SINGLE CONNECTION EXAMPLE:")
    print(data)


def pooled_connection_example():
    connection_pool = SimpleConnectionPool(1, 10,
                                           host="127.0.0.1",
                                           port=5432,
                                           dbname="test_database",
                                           user="test_user",
                                           password=os.environ.get("DB_PASSWORD", "password"))
    connection = connection_pool.getconn()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students;")
    data = cursor.fetchall()
    cursor.close()
    connection_pool.putconn(connection)
    connection_pool.closeall()
    print("POOLED CONNECTION EXAMPLE:")
    print(data)


if __name__ == "__main__":
    main()
