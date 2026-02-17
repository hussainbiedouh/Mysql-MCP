# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release preparation

## [1.0.0] - 2024-01-15

### Added

- Initial release of MySQL MCP Server
- `mysql_connect` - Connect to MySQL databases and test connections
- `mysql_query` - Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
- `mysql_list_databases` - List all databases on the server
- `mysql_list_tables` - List all tables in a database
- `mysql_describe_table` - Get schema/structure of a table
- `mysql_create_database` - Create new databases
- `mysql_drop_database` - Drop/delete databases
- `mysql_create_table` - Create new tables with custom schema
- `mysql_drop_table` - Drop/delete tables
- JSON-safe serialization for datetime, date, time, and Decimal types
- MCP server implementation with stdio transport
- Configuration files for multiple MCP clients:
  - Claude Code
  - Cursor IDE
  - Generic MCP clients
  - UV-based installations
- Comprehensive test suite (13 tests)
- Setup scripts for Windows and Unix
- Documentation and usage examples

### Security

- Parameterized connection handling
- Error messages sanitized before returning

---

## Version History Summary

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2024-01-15 | Initial release |

---

[Unreleased]: https://github.com/hussainbiedouh/Mysql-MCP/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hussainbiedouh/Mysql-MCP/releases/tag/v1.0.0