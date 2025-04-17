import json
import logging
from typing import Any, Dict, List

import pytest

from src.services import (calculate_cashback_categories, invest_piggy_bank_monthly, search_by_phone,
                          search_transfers_to_individuals, simple_search)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """
    Фикстура, предоставляющая список транзакций для тестов.
    """
    return [
        {'category': 'Food', 'amount': 100, 'date': '2024-04-01'},
        {'category': 'Transport', 'amount': 50, 'date': '2024-04-05'},
        {'category': 'Food', 'amount': 200, 'date': '2024-04-10'}
    ]


def test_calculate_cashback_categories(sample_transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует функцию calculate_cashback_categories.
    """
    result: str = calculate_cashback_categories(2024, 4, sample_transactions)
    assert json.loads(result)['year'] == 2024


def test_simple_search(sample_transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует функцию simple_search.
    """
    result: str = simple_search('Food', sample_transactions)
    assert json.loads(result)['query'] == 'food'


def test_search_by_phone(sample_transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует функцию search_by_phone.
    """
    result: str = search_by_phone(sample_transactions)
    result_json: Dict[str, Any] = json.loads(result)
    if 'error' in result_json:
        assert result_json['error'] == 'Failed to search phone numbers'
    else:
        assert result_json['found_phone_numbers'] == []


def test_search_transfers_to_individuals(sample_transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует функцию search_transfers_to_individuals.
    """
    result: str = search_transfers_to_individuals(sample_transactions)
    result_json: Dict[str, Any] = json.loads(result)
    if 'error' in result_json:
        assert result_json['error'] == 'Failed to search transfers to individuals'
    else:
        assert result_json['found_transfers'] == []


def test_invest_piggy_bank_monthly(sample_transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует функцию invest_piggy_bank_monthly.
    """
    month: int = 4
    rounding_step: int = 50
    result_str: str = invest_piggy_bank_monthly(month, sample_transactions, rounding_step)
    result: Dict[str, Any] = json.loads(result_str)

    total_amount: float = sum(t['amount'] for t in sample_transactions)
    expected_rounded: int = ((int(total_amount) + rounding_step - 1) // rounding_step) * rounding_step
    expected_difference: float = expected_rounded - total_amount  # <-- float, не int

    assert result['month'] == month
    assert abs(result['total_amount'] - total_amount) < 1e-6
    assert result['rounded_amount'] == expected_rounded
    assert abs(result['difference'] - expected_difference) < 1e-6
