@echo off
echo ==========================================
echo MySQL MCP Server Setup
echo ==========================================
echo.

REM Check if uv is installed
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] UV is not installed. Please install it first:
    echo   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    exit /b 1
)

echo [1/4] Creating virtual environment...
uv venv

echo [2/4] Installing dependencies...
uv pip install -e ".[dev]"

echo [3/4] Verifying installation...
python -c "from mysql_mcp.utils import connect, query, list_databases; print('OK Imports successful')"

echo [4/4] Running tests...
python -m pytest tests/ -v

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To start the MCP server, run:
echo   mysql-mcp
echo   or: python -m mysql_mcp.server
echo.
echo To use with Claude Code, add to settings:
echo   Copy mcp-configs\claude-code.json to your Claude config
echo.