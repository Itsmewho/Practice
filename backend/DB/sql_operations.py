import psycopg2

from psycopg2 import OperationalError, ProgrammingError, DatabaseError
from utils.utils import red, reset, green, yellow, blue, setup_logger
from connections.postSQL import get_db_connection


logger = setup_logger(__name__)


def execute_query(query, params=None, fetch=False, fetchall=False):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())

                if fetch:
                    result = cursor.fetchone()
                    logger.info(green + "Query executed (fetch one)" + reset)
                    return result

                if fetchall:
                    result = cursor.fetchall()
                    logger.info(
                        green
                        + f"Query executed (fetch all)  {len(result)} rows"
                        + reset
                    )
                    return result

                conn.commit()
                logger.info(yellow + "Query executed and committed." + reset)

    except (OperationalError, ProgrammingError) as db_error:
        logger.error(red + f"DB error during query: {db_error}" + reset)
    except DatabaseError as general_db_error:
        logger.error(red + f"General database error: {general_db_error}" + reset)
    except Exception as e:
        logger.error(red + f"Unexpected error during query: {e}" + reset)

    return None


def insert_record(table_name, columns, values):
    try:
        placeholders = ",".join(["%s"] * len(values))
        column_names = ",".join(columns)
        query = f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders}) RETURNING id;'
        logger.info(blue + f"Inserting record into {table_name}..." + reset)
        return execute_query(query, values, fetch=True)
    except Exception as e:
        logger.error(red + f"Insert failed: {e}" + reset)
        return None


def fetch_records(table_name, columns="*", where_clause=None, params=None, limit=None):
    try:
        query = f'SELECT {columns} FROM "{table_name}"'
        if where_clause:
            query += f" WHERE {where_clause}"
        if limit:
            query += f" LIMIT {limit}"
        logger.info(blue + f"Fetching records from {table_name}..." + reset)
        return execute_query(query, params, fetchall=True)
    except Exception as e:
        logger.error(red + f"Fetch failed for {table_name}: {e}" + reset)
        return []


def update_records(table_name, set_clause, where_clause, params):
    try:
        query = f'UPDATE "{table_name}" SET {set_clause} WHERE {where_clause}'
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                updated = cursor.rowcount
                logger.info(
                    green + f"{updated} row(s) updated in {table_name}." + reset
                )
                return updated > 0
    except Exception as e:
        logger.error(red + f"Update failed in {table_name}: {e}" + reset)
        return False


def delete_records(table_name, where_clause=None, params=None):
    try:
        query = f'DELETE FROM "{table_name}"'
        if where_clause:
            query += f" WHERE {where_clause}"
        logger.info(yellow + f"Deleting from {table_name}..." + reset)
        return execute_query(query, params)
    except Exception as e:
        logger.error(red + f"Delete failed in {table_name}: {e}" + reset)
        return False
