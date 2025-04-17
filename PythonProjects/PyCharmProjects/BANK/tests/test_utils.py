import datetime
import json
from typing import Any, Dict, Optional
from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests

from src.utils import get_data_from_api, process_dataframe, process_date, to_json


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """
    Фикстура, создающая DataFrame с примером данных для тестов.
    """
    data: Dict[str, Any] = {
        'date': [datetime.datetime(2024, 4, 1), datetime.datetime(2024, 4, 2)],
        'category': ['Food', 'Transport'],
        'amount': [100, 50]
    }
    df: pd.DataFrame = pd.DataFrame(data)
    return df


def test_get_data_from_api_success() -> None:
    """
    Тестирует успешное получение данных из API.
    """
    # Мокаем успешный ответ API
    mock_response: Mock = Mock()
    mock_response.json.return_value = {'data': 'value'}
    mock_response.raise_for_status = Mock()
    with patch('requests.get', return_value=mock_response):
        result: Optional[Dict[str, Any]] = get_data_from_api('https://example.com/api/data')
        assert result == {'data': 'value'}


def test_get_data_from_api_failure() -> None:
    """
    Тестирует ситуацию, когда не удается получить данные из API.
    """
    # Мокаем ошибку запроса
    with patch('requests.get', side_effect=requests.RequestException("Ошибка сети")):
        result: Optional[Dict[str, Any]] = get_data_from_api('https://example.com/api/data')
        assert result is None


def test_process_date() -> None:
    """
    Тестирует функцию process_date с корректной датой.
    """
    result: Optional[datetime.datetime] = process_date('2024-04-01 12:00:00')
    assert isinstance(result, datetime.datetime)


def test_process_date_invalid() -> None:
    """
    Тестирует функцию process_date с некорректной датой.
    """
    result: Optional[datetime.datetime] = process_date('invalid-date')
    assert result is None


def test_process_dataframe(sample_df: pd.DataFrame) -> None:
    """
    Тестирует функцию process_dataframe.
    """
    result: pd.DataFrame = process_dataframe(sample_df)
    assert 'new_column' in result.columns
    assert all(result['new_column'] == 'example')


def test_to_json() -> None:
    """
    Тестирует функцию to_json.
    """
    data: Dict[str, str] = {'key': 'value'}
    result: str = to_json(data)
    assert json.loads(result) == data
