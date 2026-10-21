# MySQL MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-13%20passed-brightgreen.svg)](tests/)

A **Model Context Protocol (MCP)** server for MySQL database operations. Enable your AI assistants to interact with MySQL databases directly.

## Features

- **Connect** to MySQL databases and test connections
- **Query** execution (SELECT, INSERT, UPDATE, DELETE)
- **List** databases and tables
- **Describe** table schemas
- **Create/Drop** databases and tables
- **JSON-safe** serialization for datetime and decimal types

## Installation

### Prerequisites

- Python 3.10 or higher
- MySQL server (8.0+ recommended)
- [UV package manager](https://docs.astral.sh/uv/) (recommended) or pip

### Quick Start

**Windows:**
```batch
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/hussainbiedouh/Mysql-MCP.git
cd Mysql-MCP

# Create virtual environment
uv venv

# Install the package
uv pip install -e ".[dev]"

# Verify installation
python -c "from mysql_mcp.utils import connect; print('Installation successful!')"
```

## Configuration

### MCP Client Setup

Choose the appropriate configuration file from `mcp-configs/`:

| Client | Config File | Description |
|--------|-------------|-------------|
| OpenCode | `opencode.json` | OpenCode, nested under `mcp.servers` |
| Claude Code | `claude-code.json` | Anthropic's Claude Code |
| Cursor | `cursor.json` | Cursor IDE |
| Generic MCP | `generic-mcp.json` | Any MCP-compatible client |
| UV-based | `uv_generic.json` | Using UV package manager |

#### Example Configuration (Claude Code)

```json
{
  "mcpServers": {
    "mysql-mcp": {
      "name": "MySQL MCP",
      "description": "MySQL database operations server",
      "command": "C:\\path\\to\\mysql-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "mysql_mcp.server"],
      "cwd": "C:\\path\\to\\mysql-mcp",
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

#### Example Configuration (OpenCode)

OpenCode nests servers under `mcp.servers` in `~/.config/opencode/opencode.jsonc`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "mysql-mcp": {
        "type": "local",
        "command": [
          "C:\\path\\to\\mysql-mcp\\.venv\\Scripts\\python.exe",
          "-m",
          "mysql_mcp.server"
        ],
        "cwd": "C:\\path\\to\\mysql-mcp",
        "environment": {
          "PYTHONIOENCODING": "utf-8"
        }
      }
    }
  }
}
```

Every client expects a different key, so the same file will not work across all of them. [mcp-client-config](https://github.com/hussainbiedouh/mcp-client-config) has the full table and what each failure mode looks like.

## Available Tools

### Connection Tools

#### `mysql_connect`
Connect to a MySQL database and test the connection.

```json
{
  "host": "localhost",
  "port": 3306,
  "username": "root",
  "password": "your_password",
  "database": "optional_database"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Connected to MySQL Server version 8.0.35",
  "database": "optional_database"
}
```

### Query Tools

#### `mysql_query`
Execute SQL queries (SELECT, INSERT, UPDATE, DELETE).

```json
{
  "host": "localhost",
  "port": 3306,
  "username": "root",
  "password": "your_password",
  "database": "mydb",
  "query": "SELECT * FROM users WHERE active = true LIMIT 10"
}
```

**SELECT Response:**
```json
{
  "success": true,
  "rows": [...],
  "row_count": 5
}
```

**INSERT/UPDATE/DELETE Response:**
```json
{
  "success": true,
  "affected_rows": 3,
  "last_insert_id": 42,
  "message": "Query executed successfully. 3 row(s) affected."
}
```

### Database Management Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `mysql_list_databases` | List all databases on server | `host`, `port`, `username`, `password` |
| `mysql_create_database` | Create a new database | + `database` |
| `mysql_drop_database` | Delete a database | + `database` |

### Table Management Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `mysql_list_tables` | List tables in a database | `host`, `port`, `username`, `password`, `database` |
| `mysql_describe_table` | Get table schema | + `table` |
| `mysql_create_table` | Create a new table | + `table`, `schema` |
| `mysql_drop_table` | Delete a table | + `table` |

#### Example: Create Table

```json
{
  "host": "localhost",
  "port": 3306,
  "username": "root",
  "password": "your_password",
  "database": "mydb",
  "table": "users",
  "schema": "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}
```

## Usage Examples

### Connecting to a Database

```python
# Via MCP tool call
{
  "tool": "mysql_connect",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "secret",
    "database": "production"
  }
}
```

### Running Queries

```json
// Simple SELECT
{
  "tool": "mysql_query",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "secret",
    "database": "myapp",
    "query": "SELECT id, name, email FROM users WHERE status = 'active' ORDER BY created_at DESC"
  }
}

// INSERT with auto-increment
{
  "tool": "mysql_query",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "secret",
    "database": "myapp",
    "query": "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com')"
  }
}

// UPDATE
{
  "tool": "mysql_query",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "secret",
    "database": "myapp",
    "query": "UPDATE users SET last_login = NOW() WHERE id = 42"
  }
}
```

### Exploring Schema

```json
// List all databases
{
  "tool": "mysql_list_databases",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "secret"
  }
}

// List tables in a database
{
  "tool": "mysql_list_tables",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "secret",
    "database": "myapp"
  }
}

// Describe a table
{
  "tool": "mysql_describe_table",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "secret",
    "database": "myapp",
    "table": "users"
  }
}
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=mysql_mcp
```

### Code Quality

```bash
# Linting
ruff check src/

# Format code
ruff format src/

# Type checking
mypy src/
```

### Project Structure

```
mysql-mcp/
├── src/mysql_mcp/
│   ├── __init__.py      # Package initialization
│   ├── server.py        # MCP server implementation
│   └── utils.py         # MySQL utility functions
├── mcp-configs/         # MCP client configurations
│   ├── claude-code.json
│   ├── cursor.json
│   ├── generic-mcp.json
│   └── uv_generic.json
├── tests/
│   ├── __init__.py
│   └── test_utils.py    # Unit tests
├── pyproject.toml       # Package configuration
├── setup.bat            # Windows setup script
├── setup.sh             # Unix setup script
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## Security Considerations

> **Warning:** This server transmits database credentials and queries. Consider the following:

1. **Local Development Only** - Recommended for local development environments
2. **Credential Management** - Use environment variables or secure credential storage
3. **Network Security** - Ensure MySQL connections use SSL/TLS in production
4. **Access Control** - Use MySQL users with minimal required permissions
5. **Query Validation** - The server does not validate or sanitize queries

### Recommended MySQL User Setup

```sql
-- Create a limited user for MCP operations
CREATE USER 'mcp_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON your_database.* TO 'mcp_user'@'localhost';
-- For schema operations, add:
GRANT CREATE, DROP, ALTER ON your_database.* TO 'mcp_user'@'localhost';
FLUSH PRIVILEGES;
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'mysql.connector'` | Run `uv pip install mysql-connector-python` |
| `Access denied for user` | Check username/password and MySQL permissions |
| `Can't connect to MySQL server` | Verify host, port, and that MySQL is running |
| `Unknown database` | Create the database first or check spelling |

### Connection String Format

If you have a connection string, parse it:
```
mysql://username:password@host:port/database
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
- Inspired by the MCP server architecture