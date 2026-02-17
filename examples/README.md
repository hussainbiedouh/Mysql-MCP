# MySQL MCP Examples

This directory contains example usage patterns for the MySQL MCP Server.

## Files

| File | Description |
|------|-------------|
| `example_usage.py` | Python file with all tool examples |
| `quickstart.md` | Quick start guide with common scenarios |

## Quick Examples

### Connect to Database

```json
{
  "tool": "mysql_connect",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "your_password",
    "database": "mydb"
  }
}
```

### Execute Query

```json
{
  "tool": "mysql_query",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "your_password",
    "database": "mydb",
    "query": "SELECT * FROM users LIMIT 10"
  }
}
```

### List Tables

```json
{
  "tool": "mysql_list_tables",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "your_password",
    "database": "mydb"
  }
}
```

### Create Table

```json
{
  "tool": "mysql_create_table",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "your_password",
    "database": "mydb",
    "table": "users",
    "schema": "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255) UNIQUE"
  }
}
```

## Common Workflows

### 1. Explore Unknown Database

1. `mysql_list_databases` - See what databases exist
2. `mysql_list_tables` - See tables in a database
3. `mysql_describe_table` - Understand table structure
4. `mysql_query` - Sample some data

### 2. Setup New Application

1. `mysql_create_database` - Create database
2. `mysql_create_table` - Create tables
3. `mysql_query` (INSERT) - Seed initial data

### 3. Data Analysis

1. `mysql_query` (SELECT) - Retrieve data
2. Multiple queries for analysis