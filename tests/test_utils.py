"""Tests for MySQL MCP utilities."""

import pytest
from datetime import datetime, date
from decimal import Decimal

from mysql_mcp.utils import convert_to_json_safe


class TestConvertToJsonSafe:
    """Tests for the convert_to_json_safe function."""

    def test_none_value(self):
        """Test that None is returned as is."""
        assert convert_to_json_safe(None) is None

    def test_string_value(self):
        """Test that strings are returned as is."""
        assert convert_to_json_safe("hello") == "hello"

    def test_integer_value(self):
        """Test that integers are returned as is."""
        assert convert_to_json_safe(42) == 42

    def test_float_value(self):
        """Test that floats are returned as is."""
        assert convert_to_json_safe(3.14) == 3.14

    def test_boolean_value(self):
        """Test that booleans are returned as is."""
        assert convert_to_json_safe(True) is True
        assert convert_to_json_safe(False) is False

    def test_datetime_value(self):
        """Test that datetime is converted to ISO format string."""
        dt = datetime(2024, 1, 15, 10, 30, 45)
        result = convert_to_json_safe(dt)
        assert result == "2024-01-15T10:30:45"
        assert isinstance(result, str)

    def test_date_value(self):
        """Test that date is converted to ISO format string."""
        d = date(2024, 1, 15)
        result = convert_to_json_safe(d)
        assert result == "2024-01-15"
        assert isinstance(result, str)

    def test_decimal_value(self):
        """Test that Decimal is converted to float."""
        dec = Decimal("123.45")
        result = convert_to_json_safe(dec)
        assert result == 123.45
        assert isinstance(result, float)

    def test_list_value(self):
        """Test that list items are converted recursively."""
        data = [
            datetime(2024, 1, 15),
            Decimal("99.99"),
            "string",
            42,
            None
        ]
        result = convert_to_json_safe(data)
        assert result == [
            "2024-01-15T00:00:00",
            99.99,
            "string",
            42,
            None
        ]

    def test_dict_value(self):
        """Test that dict values are converted recursively."""
        data = {
            "date": date(2024, 1, 15),
            "amount": Decimal("50.00"),
            "name": "test",
            "count": 10,
            "active": True
        }
        result = convert_to_json_safe(data)
        assert result == {
            "date": "2024-01-15",
            "amount": 50.0,
            "name": "test",
            "count": 10,
            "active": True
        }

    def test_nested_structure(self):
        """Test that nested structures are converted properly."""
        data = {
            "records": [
                {"id": 1, "created_at": datetime(2024, 1, 15, 12, 0, 0)},
                {"id": 2, "created_at": datetime(2024, 1, 16, 13, 30, 0)},
            ],
            "total": Decimal("150.75"),
            "metadata": {
                "last_updated": date(2024, 1, 20)
            }
        }
        result = convert_to_json_safe(data)
        assert result == {
            "records": [
                {"id": 1, "created_at": "2024-01-15T12:00:00"},
                {"id": 2, "created_at": "2024-01-16T13:30:00"},
            ],
            "total": 150.75,
            "metadata": {
                "last_updated": "2024-01-20"
            }
        }

    def test_empty_list(self):
        """Test that empty lists are handled."""
        assert convert_to_json_safe([]) == []

    def test_empty_dict(self):
        """Test that empty dicts are handled."""
        assert convert_to_json_safe({}) == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])