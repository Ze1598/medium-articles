from configparser import ConfigParser
import psycopg2
from typing import Dict


def load_connection_info(
    ini_filename: str
) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "postgresql" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info


def create_db(
    conn_info: Dict[str, str],
) -> None:
    # Connect just to PostgreSQL with the user loaded from the .ini file
    psql_connection_string = f"user={conn_info['user']} password={conn_info['password']}"
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()

    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {conn_info['database']}"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False


def create_table(
    sql_query: str, 
    conn: psycopg2.extensions.connection, 
    cur: psycopg2.extensions.cursor
) -> None:
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()


if __name__ == "__main__":
    # host, database, user, password
    conn_info = load_connection_info("db.ini")

    # Create the desired database
    create_db(conn_info)

    # Connect to the database created
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    # Create the "house" table
    house_sql = """
        CREATE TABLE house (
            id SERIAL PRIMARY KEY,
            address VARCHAR(200) UNIQUE NOT NULL
        )
    """
    create_table(house_sql, connection, cursor)


    # Create the "person" table
    person_sql = """
        CREATE TABLE person (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            house_id SERIAL REFERENCES house(id)
        )
    """
    create_table(person_sql, connection, cursor)

    # Close all connections to the database
    connection.close()
    cursor.close()
