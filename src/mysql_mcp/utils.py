"""
Utility functions for MySQL database operations.
"""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

import mysql.connector
from mysql.connector import Error


def convert_to_json_safe(obj: Any) -> Any:
    """
    Convert objects to JSON-safe representations.

    Handles datetime, date, time, Decimal, and nested structures.

    Args:
        obj: Object to convert

    Returns:
        JSON-safe representation of the object
    """
    if isinstance(obj, list):
        return [convert_to_json_safe(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_to_json_safe(value) for key, value in obj.items()}
    elif isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif obj is None:
        return None
    else:
        return obj


def connect(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str | None = None,
) -> dict[str, Any]:
    """
    Test connection to MySQL database.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Optional database name to connect to

    Returns:
        Dictionary with connection result
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            connection.close()
            return {
                "success": True,
                "message": f"Connected to MySQL Server version {db_info}",
                "database": database or "No database selected",
            }
    except Error as e:
        return {"success": False, "error": str(e)}


def query(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
    sql_query: str,
) -> dict[str, Any]:
    """
    Execute a SQL query on the database.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Database name
        sql_query: SQL query to execute

    Returns:
        Dictionary with query result
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
        )
        cursor = connection.cursor(dictionary=True)

        # Determine if this is a SELECT query
        is_select = sql_query.strip().upper().startswith("SELECT")

        cursor.execute(sql_query)

        if is_select:
            results = cursor.fetchall()
            # Convert datetime objects to strings for JSON serialization
            results = convert_to_json_safe(results)
            connection.close()
            return {
                "success": True,
                "rows": results,
                "row_count": len(results),
            }
        else:
            # For INSERT, UPDATE, DELETE
            connection.commit()
            affected_rows = cursor.rowcount
            last_id = cursor.lastrowid
            connection.close()
            return {
                "success": True,
                "affected_rows": affected_rows,
                "last_insert_id": last_id,
                "message": f"Query executed successfully. {affected_rows} row(s) affected.",
            }
    except Error as e:
        return {"success": False, "error": str(e)}


def list_databases(
    host: str,
    port: int,
    username: str,
    password: str,
) -> dict[str, Any]:
    """
    List all databases on the server.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password

    Returns:
        Dictionary with list of databases
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
        )
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        connection.close()
        return {
            "success": True,
            "databases": databases,
            "count": len(databases),
        }
    except Error as e:
        return {"success": False, "error": str(e)}


def list_tables(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
) -> dict[str, Any]:
    """
    List all tables in a database.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Database name

    Returns:
        Dictionary with list of tables
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        connection.close()
        return {
            "success": True,
            "database": database,
            "tables": tables,
            "count": len(tables),
        }
    except Error as e:
        return {"success": False, "error": str(e)}


def describe_table(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
    table: str,
) -> dict[str, Any]:
    """
    Get the schema of a table.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Database name
        table: Table name

    Returns:
        Dictionary with table schema
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        # Convert any non-serializable types
        columns = convert_to_json_safe(columns)
        connection.close()
        return {
            "success": True,
            "table": table,
            "columns": columns,
        }
    except Error as e:
        return {"success": False, "error": str(e)}


def create_database(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
) -> dict[str, Any]:
    """
    Create a new database.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Database name to create

    Returns:
        Dictionary with result
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {database}")
        connection.close()
        return {
            "success": True,
            "message": f"Database '{database}' created successfully",
        }
    except Error as e:
        return {"success": False, "error": str(e)}


def drop_database(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
) -> dict[str, Any]:
    """
    Drop/delete a database.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Database name to drop

    Returns:
        Dictionary with result
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
        )
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE {database}")
        connection.close()
        return {
            "success": True,
            "message": f"Database '{database}' dropped successfully",
        }
    except Error as e:
        return {"success": False, "error": str(e)}


def create_table(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
    table: str,
    schema: str,
) -> dict[str, Any]:
    """
    Create a new table.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Database name
        table: Table name to create
        schema: Table schema definition

    Returns:
        Dictionary with result
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
        )
        cursor = connection.cursor()
        create_sql = f"CREATE TABLE {table} ({schema})"
        cursor.execute(create_sql)
        connection.close()
        return {
            "success": True,
            "message": f"Table '{table}' created successfully",
        }
    except Error as e:
        return {"success": False, "error": str(e)}


def drop_table(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
    table: str,
) -> dict[str, Any]:
    """
    Drop/delete a table.

    Args:
        host: MySQL server host
        port: MySQL server port
        username: MySQL username
        password: MySQL password
        database: Database name
        table: Table name to drop

    Returns:
        Dictionary with result
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
        )
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE {table}")
        connection.close()
        return {
            "success": True,
            "message": f"Table '{table}' dropped successfully",
        }
    except Error as e:
        return {"success": False, "error": str(e)}
