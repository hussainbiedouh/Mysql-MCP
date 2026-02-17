#!/usr/bin/env python3
"""
MySQL MCP Server
A Model Context Protocol server for MySQL database operations.
"""

import asyncio
import json
from typing import Any

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    TextContent,
    Tool,
)

from .utils import (
    connect,
    create_database,
    create_table,
    describe_table,
    drop_database,
    drop_table,
    list_databases,
    list_tables,
    query,
)

# Server instance
server = Server("mysql-mcp")


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="mysql-mcp://docs",
            name="MySQL MCP Documentation",
            description="Documentation for the MySQL MCP server",
            mimeType="text/plain",
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: Any) -> str:
    """Read a resource by URI."""
    if str(uri) == "mysql-mcp://docs":
        return """
# MySQL MCP Server

Available tools:
- mysql_connect: Connect to a MySQL database and test the connection
- mysql_query: Execute a SQL query on a MySQL database (SELECT, INSERT, UPDATE, DELETE)
- mysql_list_databases: List all databases on the MySQL server
- mysql_list_tables: List all tables in a MySQL database
- mysql_describe_table: Get the schema/structure of a MySQL table
- mysql_create_database: Create a new MySQL database
- mysql_drop_database: Drop/delete a MySQL database
- mysql_create_table: Create a new MySQL table
- mysql_drop_table: Drop/delete a MySQL table

All tools require connection parameters: host, port, username, password.
"""
    raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="mysql_connect",
            description="Connect to a MySQL database and test the connection",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name to connect to (optional)",
                    },
                },
                "required": ["host", "port", "username", "password"],
            },
        ),
        Tool(
            name="mysql_query",
            description="Execute a SQL query on a MySQL database (SELECT, INSERT, UPDATE, DELETE)",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name",
                    },
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute",
                    },
                },
                "required": ["host", "port", "username", "password", "database", "query"],
            },
        ),
        Tool(
            name="mysql_list_databases",
            description="List all databases on the MySQL server",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                },
                "required": ["host", "port", "username", "password"],
            },
        ),
        Tool(
            name="mysql_list_tables",
            description="List all tables in a MySQL database",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name",
                    },
                },
                "required": ["host", "port", "username", "password", "database"],
            },
        ),
        Tool(
            name="mysql_describe_table",
            description="Get the schema/structure of a MySQL table",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name",
                    },
                    "table": {
                        "type": "string",
                        "description": "Table name to describe",
                    },
                },
                "required": ["host", "port", "username", "password", "database", "table"],
            },
        ),
        Tool(
            name="mysql_create_database",
            description="Create a new MySQL database",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name to create",
                    },
                },
                "required": ["host", "port", "username", "password", "database"],
            },
        ),
        Tool(
            name="mysql_drop_database",
            description="Drop/delete a MySQL database",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name to drop",
                    },
                },
                "required": ["host", "port", "username", "password", "database"],
            },
        ),
        Tool(
            name="mysql_create_table",
            description="Create a new MySQL table",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name",
                    },
                    "table": {
                        "type": "string",
                        "description": "Table name to create",
                    },
                    "schema": {
                        "type": "string",
                        "description": "Table schema definition (e.g., 'id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255)')",
                    },
                },
                "required": ["host", "port", "username", "password", "database", "table", "schema"],
            },
        ),
        Tool(
            name="mysql_drop_table",
            description="Drop/delete a MySQL table",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "MySQL server host",
                    },
                    "port": {
                        "type": "integer",
                        "description": "MySQL server port (default: 3306)",
                    },
                    "username": {
                        "type": "string",
                        "description": "MySQL username",
                    },
                    "password": {
                        "type": "string",
                        "description": "MySQL password",
                    },
                    "database": {
                        "type": "string",
                        "description": "Database name",
                    },
                    "table": {
                        "type": "string",
                        "description": "Table name to drop",
                    },
                },
                "required": ["host", "port", "username", "password", "database", "table"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    try:
        host = arguments.get("host", "localhost")
        port = arguments.get("port", 3306)
        username = arguments.get("username", "")
        password = arguments.get("password", "")
        database = arguments.get("database")
        table = arguments.get("table")
        sql_query = arguments.get("query")
        schema = arguments.get("schema")

        if name == "mysql_connect":
            result = connect(host, port, username, password, database)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_query":
            if not database or not sql_query:
                raise ValueError("database and query are required")
            result = query(host, port, username, password, database, sql_query)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_list_databases":
            result = list_databases(host, port, username, password)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_list_tables":
            if not database:
                raise ValueError("database is required")
            result = list_tables(host, port, username, password, database)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_describe_table":
            if not database or not table:
                raise ValueError("database and table are required")
            result = describe_table(host, port, username, password, database, table)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_create_database":
            if not database:
                raise ValueError("database is required")
            result = create_database(host, port, username, password, database)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_drop_database":
            if not database:
                raise ValueError("database is required")
            result = drop_database(host, port, username, password, database)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_create_table":
            if not database or not table or not schema:
                raise ValueError("database, table, and schema are required")
            result = create_table(host, port, username, password, database, table, schema)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        elif name == "mysql_drop_table":
            if not database or not table:
                raise ValueError("database and table are required")
            result = drop_table(host, port, username, password, database, table)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2),
                )
            ]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {"error": str(e), "tool": name}, indent=2
                ),
            )
        ]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mysql-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
