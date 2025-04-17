import json
from datetime import datetime
from typing import Any, Dict

import pandas as pd
import pytest

from src.reports import expenses_by_category, expenses_by_day_of_week, expenses_by_workday, spending_by_weekday


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """
    Фикстура, создающая DataFrame с примером данных для тестов.
    """
    data: Dict[str, Any] = {
        'date': [datetime(2024, 4, 1), datetime(2024, 4, 2), datetime(2024, 4, 3)],
        'category': ['Food', 'Food', 'Transport'],
        'amount': [100, 200, 50]
    }
    df: pd.DataFrame = pd.DataFrame(data)
    return df


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    """
    Фикстура, предоставляющая DataFrame с примером транзакций для тестов.
    """
    data = {'date': pd.to_datetime(['2023-12-31', '2024-01-01', '2024-01-02', '2024-01-08', '2024-01-09']),
            'amount': [50, 100, 120, 150, 180]}
    return pd.DataFrame(data)


def test_expenses_by_workday(sample_df: pd.DataFrame) -> None:
    """
    Тест функции expenses_by_workday.
    """
    result: str = expenses_by_workday(sample_df, 'Food', '2024-04-01')
    result_json: Dict[str, Any] = json.loads(result)
    assert result_json['status'] == 'success'


def test_expenses_by_category(sample_df: pd.DataFrame) -> None:
    """
    Тест функции expenses_by_category.
    """
    result: str = expenses_by_category(sample_df, 'Food', '2024-04-01')
    result_json: Dict[str, Any] = json.loads(result)
    assert result_json['status'] == 'success'


def test_expenses_by_day_of_week(sample_df: pd.DataFrame) -> None:
    """
    Тест функции expenses_by_day_of_week.
    """
    result: str = expenses_by_day_of_week(sample_df)
    result_json: Dict[str, Any] = json.loads(result)
    assert result_json['status'] == 'success'


def test_spending_by_weekday_with_data(sample_transactions: pd.DataFrame) -> None:
    """
    Тестирует функцию spending_by_weekday с данными о транзакциях.
    """
    result = spending_by_weekday(sample_transactions, date='2024-01-10')
    assert not result.empty
    assert 'weekday' in result.columns
    assert 'average_spending' in result.columns


def test_spending_by_weekday_no_data() -> None:
    """
    Тестирует функцию spending_by_weekday при отсутствии данных о транзакциях.
    """
    empty_df = pd.DataFrame(columns=['date', 'amount'])
    result = spending_by_weekday(empty_df)
    assert result.empty
    assert 'weekday' in result.columns
    assert 'average_spending' in result.columns


def test_spending_by_weekday_date_provided(sample_transactions: pd.DataFrame) -> None:
    """
    Тестирует функцию spending_by_weekday с предоставленной датой.
    """
    result = spending_by_weekday(sample_transactions, date='2024-01-05')
    assert 'weekday' in result.columns
    assert 'average_spending' in result.columns


def test_spending_by_weekday_default_date(sample_transactions: pd.DataFrame) -> None:
    """
    Тестирует функцию spending_by_weekday с использованием текущей даты по умолчанию.
    """
    result = spending_by_weekday(sample_transactions)
    assert 'weekday' in result.columns
    assert 'average_spending' in result.columns
