---
name: Bug Report
about: Report a bug in MySQL MCP
title: "[BUG] "
labels: bug
assignees: ""
---

## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Set up MySQL server with...
2. Configure MCP client...
3. Call tool with arguments...
4. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

What actually happened, including error messages.

## Environment

- MySQL MCP version: [e.g., 1.0.0]
- Python version: [e.g., 3.11.0]
- MySQL version: [e.g., 8.0.35]
- MCP client: [e.g., Claude Code, Cursor]
- OS: [e.g., Windows 11, Ubuntu 22.04]

## Tool Call

```json
{
  "tool": "mysql_query",
  "arguments": {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "...",
    "database": "test",
    "query": "SELECT * FROM users"
  }
}
```

## Response

```json
{
  "success": false,
  "error": "..."
}
```

## Additional Context

Add any other context about the problem here.

## Possible Solution

If you have ideas for a fix, describe them here.