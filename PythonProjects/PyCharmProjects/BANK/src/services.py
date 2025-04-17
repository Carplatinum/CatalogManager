import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_cashback_categories(year: int, month: int, transactions: List[Dict[str, Any]]) -> str:
    """
    Вычисляет наиболее выгодные категории для повышенного кэшбэка на основе транзакций за указанный месяц и год.
    """
    try:
        # Суммируем транзакции по категориям
        categories: Dict[str, float] = {}
        for transaction in transactions:
            category: Optional[str] = transaction.get('category')  # category может быть None
            if category is not None:
                amount: float = transaction.get('amount', 0)
                if category in categories:
                    categories[category] += amount
                else:
                    categories[category] = amount

        # Определяем топ-3 категорий с наибольшей суммой транзакций
        top_categories: List[Tuple[str, float]] = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]

        result: Dict[str, Any] = {
            'year': year,
            'month': month,
            'top_categories': top_categories
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при расчете выгодных категорий: {e}")
        return json.dumps({'error': 'Не удалось рассчитать категории кэшбэка'}, ensure_ascii=False)


def invest_piggy_bank(month: int, transactions: List[Dict[str, Any]], rounding_limit: int) -> str:
    """
    Рассчитывает сумму для инвестиционной копилки на основе округления общей суммы транзакций за месяц.
    """
    try:
        # Вычисляем общую сумму транзакций и округляем её
        total_amount: float = sum(transaction.get('amount', 0) for transaction in transactions)
        rounded_amount: float = round(total_amount, rounding_limit)

        result: Dict[str, Any] = {
            'month': month,
            'total_amount': total_amount,
            'rounded_amount': rounded_amount
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при расчете инвесткопилки: {e}")
        return json.dumps({'error': 'Не удалось рассчитать сумму для инвесткопилки'}, ensure_ascii=False)


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> str:
    """
    Выполняет простой поиск транзакций по запросу.
    """
    try:
        # Ищем транзакции, содержащие запрос в описании
        search_query: str = query.lower()
        found_transactions: List[Dict[str, Any]] = [
            transaction for transaction in transactions if search_query in str(transaction).lower()
        ]

        result: Dict[str, Any] = {
            'query': search_query,
            'found_transactions': found_transactions
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при поиске транзакций: {e}")
        return json.dumps({'error': 'Не удалось выполнить поиск транзакций'}, ensure_ascii=False)


def search_by_phone(transactions: List[Dict[str, Any]]) -> str:
    """
    Ищет телефонные номера в данных транзакций.
    """
    try:
        # Более строгий паттерн для телефонов (пример для РФ)
        phone_pattern = re.compile(
            r'(\+7|8)?[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}'
        )

        found_numbers = []
        for transaction in transactions:
            for key, value in transaction.items():
                # Проверяем только поля, которые могут содержать телефон
                if key.lower() in ['description', 'comment', 'note', 'phone'] and isinstance(value, str):
                    numbers = phone_pattern.findall(value)
                    found_numbers.extend(numbers)

        result = {'found_phone_numbers': found_numbers}
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при поиске телефонных номеров: {e}")
        return json.dumps({'error': 'Не удалось выполнить поиск телефонных номеров'}, ensure_ascii=False)


def search_transfers_to_individuals(transactions: List[Dict[str, Any]]) -> str:
    """
    Ищет переводы физическим лицам в данных транзакций.
    """
    try:
        # Регулярное выражение для поиска переводов (например, по ключевым словам)
        transfer_pattern: re.Pattern = re.compile(r'перевод|transfer|payment', re.IGNORECASE)

        found_transfers: List[Dict[str, Any]] = []
        for transaction in transactions:
            for key, value in transaction.items():
                if isinstance(value, str) and transfer_pattern.search(value):
                    # Проверяем наличие ФИО или других признаков физического лица
                    if re.search(r'[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+', value, re.IGNORECASE):
                        found_transfers.append(transaction)

        result: Dict[str, Any] = {
            'found_transfers': found_transfers
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при поиске переводов физическим лицам: {e}")
        return json.dumps({'error': 'Не удалось выполнить поиск переводов физическим лицам'}, ensure_ascii=False)


def invest_piggy_bank_monthly(month: int, transactions: List[Dict[str, Any]], rounding_step: int) -> str:
    """
    Рассчитывает сумму для инвестиционной копилки за указанный месяц с округлением.
    Фильтрует транзакции по месяцу, суммирует траты, округляет сумму вверх и возвращает разницу.
    """
    try:
        # Фильтрация транзакций по месяцу
        filtered = [
            t for t in transactions
            if datetime.strptime(t['date'], '%Y-%m-%d').month == month
        ]
        total_amount = sum(t.get('amount', 0) for t in filtered)

        rounded_amount = ((int(total_amount) + rounding_step - 1) // rounding_step) * rounding_step
        difference = rounded_amount - total_amount

        result = {
            'month': month,
            'total_amount': total_amount,
            'rounded_amount': rounded_amount,
            'difference': difference
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при расчете инвесткопилки за месяц: {e}")
        return json.dumps({'error': 'Не удалось рассчитать сумму для инвесткопилки'}, ensure_ascii=False)


def invest_piggy_bank_rounding(spent_amount: float, rounding_step: int, current_balance: float) -> str:
    """
    Функция для автоматического копления в инвесткопилку через округление одной транзакции.
    """
    try:
        rounded_amount = ((int(spent_amount) + rounding_step - 1) // rounding_step) * rounding_step
        difference = rounded_amount - spent_amount
        new_balance = current_balance + difference

        result = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'spent_amount': spent_amount,
            'rounded_amount': rounded_amount,
            'difference': difference,
            'new_balance': new_balance
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка в инвесткопилке: {e}")
        return json.dumps({'error': str(e)}, ensure_ascii=False)
