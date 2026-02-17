"""
Example usage of MySQL MCP Server tools.

This file demonstrates how to use the MySQL MCP tools
through the Model Context Protocol.
"""

# =============================================================================
# CONNECTION EXAMPLES
# =============================================================================

# Test connection to MySQL server (no database selected)
CONNECT_EXAMPLE = {
    "tool": "mysql_connect",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password"
    }
}
# Response:
# {
#   "success": true,
#   "message": "Connected to MySQL Server version 8.0.35",
#   "database": "No database selected"
# }

# Connect to a specific database
CONNECT_DATABASE_EXAMPLE = {
    "tool": "mysql_connect",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp"
    }
}
# Response:
# {
#   "success": true,
#   "message": "Connected to MySQL Server version 8.0.35",
#   "database": "myapp"
# }

# =============================================================================
# QUERY EXAMPLES
# =============================================================================

# SELECT query - retrieve data
SELECT_EXAMPLE = {
    "tool": "mysql_query",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "query": "SELECT id, name, email FROM users WHERE active = true ORDER BY created_at DESC LIMIT 10"
    }
}
# Response:
# {
#   "success": true,
#   "rows": [
#     {"id": 1, "name": "John Doe", "email": "john@example.com"},
#     {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
#   ],
#   "row_count": 2
# }

# INSERT query - add new data
INSERT_EXAMPLE = {
    "tool": "mysql_query",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "query": "INSERT INTO users (name, email, active) VALUES ('Alice Johnson', 'alice@example.com', true)"
    }
}
# Response:
# {
#   "success": true,
#   "affected_rows": 1,
#   "last_insert_id": 3,
#   "message": "Query executed successfully. 1 row(s) affected."
# }

# UPDATE query - modify data
UPDATE_EXAMPLE = {
    "tool": "mysql_query",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "query": "UPDATE users SET last_login = NOW() WHERE id = 1"
    }
}
# Response:
# {
#   "success": true,
#   "affected_rows": 1,
#   "last_insert_id": 0,
#   "message": "Query executed successfully. 1 row(s) affected."
# }

# DELETE query - remove data
DELETE_EXAMPLE = {
    "tool": "mysql_query",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "query": "DELETE FROM users WHERE active = false AND created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR)"
    }
}
# Response:
# {
#   "success": true,
#   "affected_rows": 5,
#   "last_insert_id": 0,
#   "message": "Query executed successfully. 5 row(s) affected."
# }

# JOIN query - complex retrieval
JOIN_EXAMPLE = {
    "tool": "mysql_query",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "query": """
            SELECT 
                u.name,
                u.email,
                COUNT(o.id) as order_count,
                SUM(o.total) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
            HAVING order_count > 0
            ORDER BY total_spent DESC
        """
    }
}

# =============================================================================
# DATABASE MANAGEMENT EXAMPLES
# =============================================================================

# List all databases
LIST_DATABASES_EXAMPLE = {
    "tool": "mysql_list_databases",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password"
    }
}
# Response:
# {
#   "success": true,
#   "databases": ["information_schema", "mysql", "myapp", "performance_schema", "sys"],
#   "count": 5
# }

# Create a new database
CREATE_DATABASE_EXAMPLE = {
    "tool": "mysql_create_database",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "new_project"
    }
}
# Response:
# {
#   "success": true,
#   "message": "Database 'new_project' created successfully"
# }

# Drop a database (USE WITH CAUTION!)
DROP_DATABASE_EXAMPLE = {
    "tool": "mysql_drop_database",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "old_project"
    }
}
# Response:
# {
#   "success": true,
#   "message": "Database 'old_project' dropped successfully"
# }

# =============================================================================
# TABLE MANAGEMENT EXAMPLES
# =============================================================================

# List tables in a database
LIST_TABLES_EXAMPLE = {
    "tool": "mysql_list_tables",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp"
    }
}
# Response:
# {
#   "success": true,
#   "database": "myapp",
#   "tables": ["users", "orders", "products", "order_items"],
#   "count": 4
# }

# Describe a table's structure
DESCRIBE_TABLE_EXAMPLE = {
    "tool": "mysql_describe_table",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "table": "users"
    }
}
# Response:
# {
#   "success": true,
#   "table": "users",
#   "columns": [
#     {"Field": "id", "Type": "int", "Null": "NO", "Key": "PRI", "Default": null, "Extra": "auto_increment"},
#     {"Field": "name", "Type": "varchar(255)", "Null": "NO", "Key": "", "Default": null, "Extra": ""},
#     {"Field": "email", "Type": "varchar(255)", "Null": "YES", "Key": "UNI", "Default": null, "Extra": ""},
#     {"Field": "created_at", "Type": "timestamp", "Null": "YES", "Key": "", "Default": "CURRENT_TIMESTAMP", "Extra": ""}
#   ]
# }

# Create a new table
CREATE_TABLE_EXAMPLE = {
    "tool": "mysql_create_table",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "table": "products",
        "schema": """
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock INT DEFAULT 0,
            category_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_category (category_id),
            INDEX idx_price (price)
        """
    }
}
# Response:
# {
#   "success": true,
#   "message": "Table 'products' created successfully"
# }

# Drop a table (USE WITH CAUTION!)
DROP_TABLE_EXAMPLE = {
    "tool": "mysql_drop_table",
    "arguments": {
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "your_password",
        "database": "myapp",
        "table": "old_table"
    }
}
# Response:
# {
#   "success": true,
#   "message": "Table 'old_table' dropped successfully"
# }

# =============================================================================
# COMMON WORKFLOWS
# =============================================================================

# Workflow 1: Setting up a new database with tables
# Step 1: Create database
# Step 2: Create tables
# Step 3: Insert initial data

WORKFLOW_SETUP_EXAMPLE = [
    {
        "step": 1,
        "tool": "mysql_create_database",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password",
            "database": "blog"
        }
    },
    {
        "step": 2,
        "tool": "mysql_create_table",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password",
            "database": "blog",
            "table": "posts",
            "schema": "id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255) NOT NULL, content TEXT, published BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    },
    {
        "step": 3,
        "tool": "mysql_query",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password",
            "database": "blog",
            "query": "INSERT INTO posts (title, content, published) VALUES ('Welcome', 'First post!', true)"
        }
    }
]

# Workflow 2: Exploring an unknown database
# Step 1: List databases
# Step 2: Connect to specific database
# Step 3: List tables
# Step 4: Describe interesting tables
# Step 5: Query sample data

WORKFLOW_EXPLORE_EXAMPLE = [
    {
        "step": 1,
        "tool": "mysql_list_databases",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password"
        }
    },
    {
        "step": 2,
        "tool": "mysql_connect",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password",
            "database": "target_db"
        }
    },
    {
        "step": 3,
        "tool": "mysql_list_tables",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password",
            "database": "target_db"
        }
    },
    {
        "step": 4,
        "tool": "mysql_describe_table",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password",
            "database": "target_db",
            "table": "main_table"
        }
    },
    {
        "step": 5,
        "tool": "mysql_query",
        "arguments": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "your_password",
            "database": "target_db",
            "query": "SELECT * FROM main_table LIMIT 5"
        }
    }
]


if __name__ == "__main__":
    print("MySQL MCP Example Usage")
    print("=" * 50)
    print("\nThis file contains example tool calls for the MySQL MCP server.")
    print("Use these as reference when making calls through your MCP client.")
    print("\nExample tools available:")
    print("- mysql_connect")
    print("- mysql_query")
    print("- mysql_list_databases")
    print("- mysql_list_tables")
    print("- mysql_describe_table")
    print("- mysql_create_database")
    print("- mysql_drop_database")
    print("- mysql_create_table")
    print("- mysql_drop_table")