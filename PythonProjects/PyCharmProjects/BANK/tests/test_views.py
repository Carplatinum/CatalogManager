import json
from datetime import datetime
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src import views


@pytest.fixture
def mock_excel_data() -> pd.DataFrame:
    """Фикстура для создания DataFrame с тестовыми данными."""
    data: Dict[str, Any] = {'date': [datetime(2024, 7, 1)], 'amount': [100], 'category': ['Food']}
    return pd.DataFrame(data)


@pytest.fixture
def user_settings_data() -> str:
    """Фикстура для данных user_settings.json."""
    return '{"user_currencies": ["USD"], "user_stocks": ["AAPL"]}'


@patch('src.views.get_currency_rates')
@patch('src.views.get_stock_prices')
@patch("builtins.open", create=True)
def test_main(
    mock_open_file: MagicMock,
    mock_get_stock_prices: MagicMock,
    mock_get_currency_rates: MagicMock,
    user_settings_data: str,
) -> None:
    """Тест для функции main."""
    mock_get_currency_rates.return_value = [{'currency': 'USD', 'rate': 75.0}]
    mock_get_stock_prices.return_value = [{'stock': 'AAPL', 'price': 150.0}]

    # Configure the mock to return the user_settings_data when read() is called
    mock_open_file.return_value.read.return_value = user_settings_data
    mock_open_file.return_value.__enter__.return_value.read.return_value = user_settings_data
    mock_open_file.return_value.__exit__.return_value = None

    date_str: str = '2024-07-01 12:00:00'
    result: str = views.main(date_str)
    result_dict: Dict[str, Any] = json.loads(result)

    assert isinstance(result_dict, dict)
    assert 'expenses' in result_dict
    assert 'income' in result_dict
    assert 'currency_rates' in result_dict
    assert 'stock_prices' in result_dict

    mock_get_currency_rates.assert_called_once()
    mock_get_stock_prices.assert_called_once()
    mock_open_file.assert_called()
