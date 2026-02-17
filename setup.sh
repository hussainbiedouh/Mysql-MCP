#!/bin/bash
echo "=========================================="
echo "MySQL MCP Server Setup"
echo "=========================================="
echo

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "[ERROR] UV is not installed. Please install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
uv venv

echo "[2/4] Installing dependencies..."
uv pip install -e ".[dev]"

echo "[3/4] Verifying installation..."
python -c "from mysql_mcp.utils import connect, query, list_databases; print('OK Imports successful')"

echo "[4/4] Running tests..."
python -m pytest tests/ -v

echo
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo
echo "To start the MCP server, run:"
echo "  mysql-mcp"
echo "  or: python -m mysql_mcp.server"
echo
echo "To use with Claude Code, add to settings:"
echo "  Copy mcp-configs/claude-code.json to your Claude config"
echo