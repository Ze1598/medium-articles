from configparser import ConfigParser
import psycopg2
import psycopg2.extras as psql_extras
import pandas as pd
from typing import Dict


def load_connection_info(
    ini_filename: str
) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "postgresql" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info


def insert_data(
    query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    page_size: int
) -> None:
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]

    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()


if __name__ == "__main__":
    # host, database, user, password
    conn_info = load_connection_info("db.ini")
    # Connect to the "houses" database
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    # Insert data into the "house" table
    house_df = pd.DataFrame({
        "id": [1, 2, 3], 
        "address": ["Street MGS, 23", "Street JHPB, 44", "Street DS, 76"]
    })
    house_query = "INSERT INTO house(id, address) VALUES %s"
    insert_data(house_query, connection, cursor, house_df, 100)

    # Insert data into the "person" table
    person_df = pd.DataFrame({
        "id": [1, 2, 3, 4], 
        "name": ["Michael", "Jim", "Pam", "Dwight"], 
        "house_id": [1, 2, 2, 3]
    })
    person_query = "INSERT INTO person(id, name, house_id) VALUES %s"
    insert_data(person_query, connection, cursor, person_df, 100)

    # Close all connections to the database
    connection.close()
    cursor.close()
